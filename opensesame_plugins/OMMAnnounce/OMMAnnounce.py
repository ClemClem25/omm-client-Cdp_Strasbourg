# coding=utf-8

from libopensesame.py3compat import *
import sys
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from openmonkeymind import BaseOMMPlugin
from libopensesame import item_stack


class OMMAnnounce(BaseOMMPlugin, Item):

    description = u'Announce-participant plugin for Open Monkey Mind'

    def reset(self):

        self.var.omm_participant = '[participant]'
        BaseOMMPlugin.reset(self)
        
    def run(self):
        
        # We dynamically set the custom log backend module so that it's
        # automatically found by OpenSesame.
        from openmonkeymind import _omm_log_backend
        sys.modules['openexp._log.omm'] = _omm_log_backend
        # Get the experiment and patch it so that re-uses the environment of
        # the current experiment, i.e. it doesn't create its own window etc.
        exp = self._openmonkeymind.announce(self.var.omm_participant)
        item_stack.item_stack_singleton.clear = lambda: None
        exp.init_display = lambda: None
        exp.end = lambda: None
        exp.window = self.experiment.window
        exp.logfile = self.experiment.logfile
        exp.python_workspace['win'] = self.experiment.window
        exp.python_workspace['omm'] = self._openmonkeymind
        # A few back-end-specific properties need to be copied to the
        # experiment.
        if self.experiment.var.canvas_backend == 'xpyriment':
            exp.expyriment = self.experiment.expyriment
        elif self.experiment.var.canvas_backend == 'legacy':
            exp.surface = self.experiment.surface
        # The backend settings need to be copied as well, although the log 
        # backend is always set to omm.
        exp.var.log_backend = 'omm'
        for backend in [
            'canvas_backend',
            'keyboard_backend',
            'mouse_backend',
            'sampler_backend',
            'clock_backend',
            'color_backend'
        ]:
            if backend in exp.var:
                if backend in self.experiment.var:
                    exp.var.set(backend, self.experiment.var.get(backend))
                else:
                    exp.var.__delattr__(backend)
        exp.run()


class qtOMMAnnounce(OMMAnnounce, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):

        OMMAnnounce.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
