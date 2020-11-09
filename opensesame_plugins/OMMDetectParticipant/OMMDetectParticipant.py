# coding=utf-8

import time
from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libopensesame.item import Item
import detectors
from libqtopensesame.items.qtautoplugin import QtAutoPlugin

SLEEP_TIME = .05
RFID_LENGTH = 19


class OMMDetectParticipant(Item):
    
    def reset(self):
        
        self.var.detector = 'Dummy'
        self.var.serial_port = 'COM3'
        self.var.participant_variable = 'participant'
        
    def _prepare_dummy(self):
        
        from openexp.keyboard import Keyboard
        self._keyboard = Keyboard(self.experiment)
        self.run = self._run_dummy
    
    def _run_dummy(self):
        
        key, timestamp = self._keyboard.get_key()
        oslogger.info('identifier: {}'.format(key))
        self.experiment.var.set(self.var.participant_variable, key)

    def _prepare_rfid(self):
        
        import serial
        self._serial = serial.Serial(self.var.serial_port, timeout=0.01)
        self.run = self._run_rfid
    
    def _run_rfid(self):
        
        self._serial.flushInput()
        while True:
            rfid = _serial.read(RFID_LENGTH)
            if rfid:
                break
        self._serial.close()
        self.experiment.var.set(self.var.participant_variable, rfid)
    
    def prepare(self):
        
        if self.var.detector == 'RFID':
            self._prepare_rfid()
        elif self.var.detector == 'Dummy':
            self._prepare_dummy()
        else:
            raise ValueError("detector should be 'dummy' or 'rfid'")


class qtOMMDetectParticipant(OMMDetectParticipant, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):

        OMMDetectParticipant.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
