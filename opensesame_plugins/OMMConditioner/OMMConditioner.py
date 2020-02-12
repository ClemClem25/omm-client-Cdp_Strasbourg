# coding=utf-8

from libopensesame.py3compat import *
import conditioners
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin


class OMMConditioner(Item):

    description = u'Conditioner plugin for Open Monkey Mind'

    def reset(self):

        self.var.conditioner = u'Dummy'
        self.var.serial_port = 'COM4'
        self.var.reward = 'yes'
        self.var.sound = 'do nothing'
        
    def _init_conditioner(self):
        
        if hasattr(self, '_conditioner'):
            return
        if 'omm_conditioner' in self.python_workspace:
            self._conditioner = self.python_workspace['omm_conditioner']
            return
        cls = getattr(conditioners, self.var.conditioner)
        self._conditioner = cls(
            experiment=self.experiment,
            port=self.var.serial_port
        )
        self.python_workspace['omm_conditioner'] = self._conditioner
        self.experiment.cleanup_functions.append(self._conditioner.close)
        
    def prepare(self):
        
        self._init_conditioner()
        
    def run(self):

        self.set_item_onset()
        if self.var.reward == 'yes':
            self._conditioner.reward()
        if self.var.sound == 'do nothing':
            return
        if self.var.sound == 'left':
            self._conditioner.sound_left()
        elif self.var.sound == 'right':
            self._conditioner.sound_right()
        elif self.var.sound == 'both':
            self._conditioner.sound_both()
        elif self.var.sound == 'off':
            self._conditioner.sound_off()
        else:
            raise ValueError('invalid sound value: {}'.format(self.var.sound))


class qtOMMConditioner(OMMConditioner, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):

        OMMConditioner.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
