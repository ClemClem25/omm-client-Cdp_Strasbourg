# coding=utf-8

from libopensesame.py3compat import *
from conditioners._base_conditioner import BaseConditioner
from libopensesame.oslogging import oslogger


class Dummy(BaseConditioner):
    
    def reward(self):
        
        oslogger.info('reward')

    def sound_left(self):
        
        oslogger.info('sound left')

    def sound_right(self):
        
        oslogger.info('sound right')

    def sound_both(self):
        
        oslogger.info('sound both')

    def sound_off(self):
        
        oslogger.info('sound off')
