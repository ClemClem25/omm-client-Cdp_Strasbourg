# coding=utf-8

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin


class BaseOMMPlugin(object):
    
    def run(self):
        
        pass
    
    def prepare(self):
        
        self._init_omm()

    def _init_omm(self):
        
        if hasattr(self, '_openmonkeymind'):
            return
        if 'omm' in self.python_workspace:
            self._openmonkeymind = self.python_workspace['omm']
            return
        from openmonkeymind import OpenMonkeyMind
        self._openmonkeymind = OpenMonkeyMind()
        self.python_workspace['omm'] = self._openmonkeymind
