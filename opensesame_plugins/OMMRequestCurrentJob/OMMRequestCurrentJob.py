# coding=utf-8

from libopensesame.py3compat import *
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import osexception
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openmonkeymind import BaseOMMPlugin


class OMMRequestCurrentJob(BaseOMMPlugin, Item):

    description = u'Plugin to request current job for Open Monkey Mind'
        
    def prepare(self):

        BaseOMMPlugin.prepare(self)
        if self._openmonkeymind.current_participant is None:
            oslogger.info('running in test mode')
            self._prepare_test()
            return
        jobs = self._openmonkeymind.request_current_job()
        for key, val in jobs.items():
            self.experiment.var.set(key, val)
            
    def _prepare_test(self):
        
        dm = self.experiment.items[
            self.var.test_loop
        ]._create_live_datamatrix()
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
