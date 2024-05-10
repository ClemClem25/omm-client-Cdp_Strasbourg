import random
from libopensesame.py3compat import *
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import OSException
from libopensesame.inline_script import inline_script as InlineScript
from openmonkeymind import BaseOMMPlugin


IGNORE_KEYS = (
    'omm_job_index',
    'omm_block_index',
    'omm_job_index_in_block'
)


class OmmRequestJob(BaseOMMPlugin, InlineScript):

    description = 'Plugin to request a job for Open Monkey Mind'
    
    def reset(self):
        
        self.var.job_index = ''
        self.var.overwrite = 'no'
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
        if self.var.job_index == '':
            self.experiment.var.omm_job_index = \
                self._openmonkeymind.get_current_job_index()
            job = self._openmonkeymind.request_job()
        else:
            self.experiment.var.omm_job_index = self.var.job_index
            job = self._openmonkeymind.request_job(self.var.job_index)
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
        for key, val in dm[0]:
            self._set_variable(key, val)
        InlineScript.prepare(self)
        
    def coroutine(self, coroutines):
        
        raise NotImplementedError()
        
    def var_info(self):
        
        return []
        
    def _set_variable(self, key, val):
        
        if key in self.experiment.var and self.var.overwrite == 'no':
            oslogger.warning('ignoring existing variable: {}'.format(key))
            return
        if key in IGNORE_KEYS:
            return
        if key == '_run':
            self.var._run = val
            return
        if key == '_prepare':
            self.var._prepare = val
            return
        if isinstance(val, basestring) and val.startswith('='):
            try:
                val = self.python_workspace._eval(val[1:])
            except Exception as e:
                raise OSException(
                    'Error evaluating Python expression in job variable',
                    line_offset=0,
                    item=self.name,
                    phase='prepare',
                    exception=e
                )
        self.experiment.var.set(key, val)
