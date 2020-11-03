# coding=utf-8

from libopensesame.py3compat import *
from openexp._log.log import Log
from libopensesame.oslogging import oslogger


class LogBackend(Log):

    def __init__(self, experiment, path):

        oslogger.info('Initializing LogBackend')
        Log.__init__(self, experiment, path)
        self._omm = self.experiment.python_workspace['omm']

    def write_vars(self, var_list=None):

        oslogger.info('Writing vars')
        if var_list is None:
            var_list = self.all_vars()
        self._omm.send_current_job_results({
            var: self.experiment.var.get(var, _eval=False, default=u'NA')
            for var in var_list
        })


# Alias for the backend class to find
omm = LogBackend
