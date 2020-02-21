# coding=utf-8

from libopensesame.py3compat import *


class BaseConditioner:
    
    def __init__(self, **kwargs):
        
        if 'experiment' not in kwargs:
            raise ValueError('BaseConditioner expects experiment keyword')
        self._experiment = kwargs['experiment']
        
    @property
    def clock(self):
        
        return self._experiment.clock        
    
    def reward(self):
        
        pass
    
    def sound_left(self):
        
        pass

    def sound_right(self):
        
        pass

    def sound_both(self):
        
        pass

    def sound_off(self):
        
        pass

    def close(self):
        
        pass
