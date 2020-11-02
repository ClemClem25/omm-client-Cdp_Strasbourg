# coding=utf-8

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openmonkeymind import BaseOMMPlugin
from libopensesame import item_stack


class OMMAnnounce(BaseOMMPlugin, Item):

    description = u'Announce-participant plugin for Open Monkey Mind'

    def reset(self):

        self.var.omm_participant = '[participant]'
        
    def run(self):

        exp = self._openmonkeymind.announce(self.var.omm_participant)
        item_stack.item_stack_singleton.clear = lambda: None
        exp.init_display = lambda: None
        exp.end = lambda: None
        if hasattr(self.experiment, 'window'):
            exp.window = self.experiment.window
            exp.python_workspace['win'] = self.experiment.window
        exp.python_workspace['omm'] = self._openmonkeymind
        exp.run()


class qtOMMAnnounce(OMMAnnounce, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):

        OMMAnnounce.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
