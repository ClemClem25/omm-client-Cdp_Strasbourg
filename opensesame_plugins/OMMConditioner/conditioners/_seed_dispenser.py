# coding=utf-8

from libopensesame.py3compat import *
from conditioners._base_conditioner import BaseConditioner
import serial

# Seed dispenser
SEED_DISPENSER_ON = b'S11'
SEED_DISPENSER_OFF = b'S10'
# Left sound
SOUND_LEFT_ON = b'S21'
SOUND_LEFT_OFF = b'S20'
# Right sound
SOUND_RIGHT_ON = b'S31'
SOUND_RIGHT_OFF = b'S30'
# What does this do?
MEMORY_ON = b'M1'
MEMORY_OFF = b'M0'
# Parameter for seed dispenser
MOTOR_N_PULSES = 5
MOTOR_PAUSE = 200


class SeedDispenser(BaseConditioner):
    
    def __init__(self, **kwargs):
        
        super(SeedDispenser, self).__init__(kwargs)
        self._port = kwargs.get('port', DEFAULT_PORT)
        self._serial = serial.Serial(self._port)
        
    def _stop(self, seed_dispenser=False, sound_left=False, sound_right=False):
        
        self._serial.write(MEMORY_OFF)
        self._serial.write(DIGITAL_ENTRY)
        self._serial.write(SEED_DISPENSER_OFF)
        self._serial.write(SOUND_LEFT_OFF)
        self._serial.write(SOUND_RIGHT_OFF)
        self._serial.flush()
        
    def reward(self):
        
        self._stop(seed_dispenser=True)
        for _ in range(MOTOR_N_PULSES):
            self._serial.write(SEED_DISPENSER_ON)
            self._serial.flush()
            self.clock.sleep(MOTOR_PAUSE)
            self._serial.write(SEED_DISPENSER_OFF)
            self._serial.flush()
            self.clock.sleep(MOTOR_PAUSE)

    def sound_left(self):
        
        self._stop(sound_right=True)
        self._serial.write(SOUND_LEFT_ON)
        self._serial.flush()

    def sound_right(self):
        
        self._stop(sound_left=True)
        self._serial.write(SOUND_RIGHT_ON)
        self._serial.flush()
        
    def sound_off(self):
        
        self._stop(sound_left=True, sound_right=True)
    
    def sound_both(self):
        
        self._serial.write(SOUND_LEFT_ON)
        self._serial.write(SOUND_RIGHT_ON)
        self._serial.flush()

    def close(self):
        
        self._serial.close()
