# coding=utf-8

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin


class BaseOMMPlugin(object):
    
    def reset(self):

        self.var.omm_server = '127.0.0.1'
        self.var.omm_port = 3000
        self.var.omm_api = 1
    
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
        self._openmonkeymind = OpenMonkeyMind(
            server=self.var.omm_server,
            port=self.var.omm_port,
            api=self.var.omm_api
        )
        self.python_workspace['omm'] = self._openmonkeymind
