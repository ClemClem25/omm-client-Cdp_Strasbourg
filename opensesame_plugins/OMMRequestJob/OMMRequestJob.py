# coding=utf-8

import random
from libopensesame.py3compat import *
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import osexception
from libopensesame.inline_script import inline_script as InlineScript
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openmonkeymind import BaseOMMPlugin


IGNORE_KEYS = (
    'omm_job_index',
    'omm_block_index',
    'omm_job_index_in_block'
)


class OMMRequestJob(BaseOMMPlugin, InlineScript):

    description = u'Plugin to request a job for Open Monkey Mind'
    
    def reset(self):
        
        self.var.block_select = 'no'
        self.var.block_size = 10
        InlineScript.reset(self)
        BaseOMMPlugin.reset(self)
        
    def run(self):
        
        InlineScript.run(self)
        
    def prepare(self):

        BaseOMMPlugin.prepare(self)
        if not self._openmonkeymind.connected:
            oslogger.info('running in test mode')
            self._prepare_test()
            return
        current_job_index = self._openmonkeymind.get_current_job_index()
        if self.var.block_select == 'no':
            self.experiment.var.omm_job_index = current_job_index
            self.experiment.var.omm_block_index = None
            self.experiment.var.omm_job_index_in_block = None
            job = self._openmonkeymind.request_job()
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
        self.experiment.var.omm_job_id = job.id_
        self.experiment.var.omm_job_count = self._openmonkeymind.job_count
        for key, val in job:
            self._set_variable(key, val)
        InlineScript.prepare(self)
        
    def _prepare_test(self):
        
        dm = self.experiment.items[
            self.var.test_loop
        ]._create_live_datamatrix()
        self.experiment.var.omm_job_index = None
        self.experiment.var.omm_job_id = None
        self.experiment.var.omm_job_count = None
        self.experiment.var.omm_block_index = None
        self.experiment.var.omm_job_index_in_block = None
        for key, val in dm[0]:
            self._set_variable(key, val)
        InlineScript.prepare(self)
        
    def coroutine(self, coroutines):
        
        raise NotImplementedError()
        
    def var_info(self):
        
        return []
        
    def _set_variable(self, key, val):
        
        if key in IGNORE_KEYS:
            return
        if key == '_run':
            self.var._run = val
            return
        if key == '_prepare':
            self.var._prepare = val
            return
        if isinstance(val, basestring) and val.startswith(u'='):
            try:
                val = self.python_workspace._eval(val[1:])
            except Exception as e:
                raise osexception(
                    u'Error evaluating Python expression in job variable',
                    line_offset=0,
                    item=self.name,
                    phase=u'prepare',
                    exception=e
                )
        self.experiment.var.set(key, val)


class qtOMMRequestJob(OMMRequestJob, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):

        OMMRequestJob.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
        
    def apply_edit_changes(self):
        
        super().apply_edit_changes()
        self.spinbox_block_size.setEnabled(self.var.block_select == 'yes')
    
    def edit_widget(self):
        
        super().edit_widget()
        self.spinbox_block_size.setEnabled(self.var.block_select == 'yes')
