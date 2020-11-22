# coding=utf-8

from libopensesame.py3compat import *
import os
from openexp._log.csv import Csv
from libopensesame.oslogging import oslogger


class LogBackend(Csv):
    
    """A log backend that sends results to the OMM server, and also writes them
    to a local file as a series JSON objects.
    """

    def __init__(self, experiment, path):

        super().__init__(experiment, path)
        self._omm = self.experiment.python_workspace['omm']
        
    def open(self, path):

        if self._log is not None:
            self.close()
        # If only a filename is present, we interpret this filename as relative
        # to the experiment folder, instead of relative to the current working
        # directory.
        if (
            os.path.basename(path) == path and
            self.experiment.experiment_path is not None
        ):
            self._path = os.path.join(self.experiment.experiment_path, path)
        else:
            self._path = path
        # Open the logfile
        self.experiment.var.logfile = self._path
        if self._path not in self.experiment.data_files:
            self.experiment.data_files.append(self._path)
        oslogger.info('appending to {}'.format(self._path))
        self._log = safe_open(self._path, u'a')

    def write_vars(self, var_list=None):

        if var_list is None:
            var_list = self.all_vars()
        json = {
            var: self.experiment.var.get(var, _eval=False, default=u'NA')
            for var in var_list
        }
        self.write(json)
        if self._omm.connected:
            self._omm.send_current_job_results(json)


# Alias for the backend class to find
omm = LogBackend
