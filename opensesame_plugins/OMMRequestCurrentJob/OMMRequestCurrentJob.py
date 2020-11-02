# coding=utf-8

import random
from libopensesame.py3compat import *
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import osexception
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openmonkeymind import BaseOMMPlugin


class OMMRequestCurrentJob(BaseOMMPlugin, Item):

    description = u'Plugin to request current job for Open Monkey Mind'
    
    def reset(self):
        
        self.var.block_select = 'no'
        self.var.block_size = 10
        
    def prepare(self):

        BaseOMMPlugin.prepare(self)
        if self._openmonkeymind.current_participant is None:
            oslogger.info('running in test mode')
            self._prepare_test()
            return
        current_job_index = self._openmonkeymind.get_current_job_index()
        if self.var.block_select == 'no':
            self.experiment.var.omm_job_index = current_job_index
            job = self._openmonkeymind.request_current_job()
        else:
            # To randomly select a job from the current block, we:
            # - Get the index of the next job
            # - Determine the block number based on this index
            # - Determine the minimum and maximum index of the block that
            #   contains this index
            # - Get all jobs within this range
            # - Shuffle these jobs, and then get the first non-finished job
            if (
                not isinstance(self.var.block_size, int) or
                self.var.block_size <= 1
            ):
                raise ValueError(
                    'block size should be an integer value larget than 1'
                )
            block_index = (current_job_index - 1) // self.var.block_size + 1
            min_job_index = (block_index - 1) * self.var.block_size + 1
            max_job_index = block_index * self.var.block_size + 1
            jobs = self._openmonkeymind.get_jobs(min_job_index, max_job_index)
            unfished_job_indices = [
                job_index + min_job_index
                for job_index, job in enumerate(jobs)
                if not job.finished
            ]
            job_index = random.choice(unfished_job_indices)
            job_index_in_block = \
                self.var.block_size - len(unfished_job_indices) + 1
            oslogger.info('global job index: {}, job index in block: {}, block index {}'.format(
                job_index,
                job_index_in_block,
                block_index
            ))
            job = self._openmonkeymind.request_job(job_index)
            self.experiment.var.omm_job_index = job_index
            self.experiment.var.omm_block_index = block_index
            self.experiment.var.omm_job_index_in_block = job_index_in_block
        for key, val in job:
            if key not in (
                'omm_job_index',
                'omm_block_index',
                'omm_job_index_in_block'
            ):
                self.experiment.var.set(key, val)
            
    def _prepare_test(self):
        
        dm = self.experiment.items[
            self.var.test_loop
        ]._create_live_datamatrix()
        self.experiment.var.omm_job_index = None
        for name, val in dm[0]:
            if isinstance(val, basestring) and val.startswith(u'='):
                try:
                    val = self.python_workspace._eval(val[1:])
                except Exception as e:
                    raise osexception(
                        u'Error evaluating Python expression in loop table',
                        line_offset=0,
                        item=self.name,
                        phase=u'run',
                        exception=e
                    )
            self.experiment.var.set(name, val)


class qtOMMRequestCurrentJob(OMMRequestCurrentJob, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):

        OMMRequestCurrentJob.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
        
    def apply_edit_changes(self):
        
        super().apply_edit_changes()
        self.spinbox_block_size.setEnabled(self.var.block_select == 'yes')
    
    def edit_widget(self):
        
        super().edit_widget()
        self.spinbox_block_size.setEnabled(self.var.block_select == 'yes')
