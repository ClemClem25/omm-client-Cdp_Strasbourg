# coding=utf-8

from libopensesame.py3compat import *
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openmonkeymind import BaseOMMPlugin


class OMMSendCurrentJobResults(BaseOMMPlugin, Item):

    description = u'Plugin to send current job results for Open Monkey Mind'
        
    def run(self):

        BaseOMMPlugin.run(self)
        if self._openmonkeymind.current_participant is None:
            oslogger.info('running in test mode')
            return
        self._openmonkeymind.send_current_job_results(
            {
                key: val
                for key, val in self.experiment.var.items()
            }
        )


class qtOMMSendCurrentJobResults(OMMSendCurrentJobResults, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):

        OMMSendCurrentJobResults.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
