# coding=utf-8

import time
from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libopensesame import widgets
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin

SLEEP_TIME = .05
RFID_LENGTH = 19


class OMMDetectParticipant(Item):
    
    def reset(self):
        
        self.var.detector = 'form'
        self.var.serial_port = 'COM3'
        self.var.participant_variable = 'participant'
        
    def _prepare_form(self):
        
        self._form = widgets.form(
            self.experiment,
            cols=(1),
            rows=(1,5),
            item=self,
            clicks=self.var.form_clicks==u'yes'
        )
        label = widgets.label(
            self._form,
            text='Enter OMM participant identifier'
        )
        self._text_input = widgets.text_input(
            self._form,
            return_accepts=True,
            var=self.var.participant_variable
        )
        self._form.set_widget(label, (0, 0))
        self._form.set_widget(self._text_input, (0, 1))
        self.run = self._run_form
        
    def _run_form(self):
        
        self._form._exec(focus_widget=self._text_input)
    
    def _prepare_keypress(self):
        
        from openexp.keyboard import Keyboard
        self._keyboard = Keyboard(self.experiment)
        self.run = self._run_keypress
    
    def _run_keypress(self):
        
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
        
        if self.var.detector == 'rfid':
            self._prepare_rfid()
        elif self.var.detector == 'keypress':
            self._prepare_keypress()
        elif self.var.detector == 'form':
            self._prepare_form()
        else:
            raise ValueError("detector should be 'Dummy', 'Form' or 'RFID'")


class qtOMMDetectParticipant(OMMDetectParticipant, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):

        OMMDetectParticipant.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
