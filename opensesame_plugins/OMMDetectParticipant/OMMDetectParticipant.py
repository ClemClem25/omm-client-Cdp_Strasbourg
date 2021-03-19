# coding=utf-8

import time
from openexp.keyboard import Keyboard
from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libopensesame import widgets
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin

RFID_LENGTH = 18    # The number of bytes of an RFID
RFID_SEP = b'\r'    # The byte that separates RFIDs in the buffer
MIN_REP = 1         # The minimum number of RFIDs that we want to read, in case
                    # we want to double-check.


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
        self.experiment.var.set(
            self.var.participant_variable,
            '/{}/'.format(self.var.get(self.var.participant_variable))
        )
    
    def _prepare_keypress(self):
        
        self._keyboard = Keyboard(self.experiment)
        self.run = self._run_keypress
    
    def _run_keypress(self):
        
        key, timestamp = self._keyboard.get_key()
        oslogger.info('identifier: {}'.format(key))
        self.experiment.var.set(
            self.var.participant_variable,
            '/{}/'.format(key)
        )

    def _prepare_rfid(self):
        
        self.run = self._run_rfid
    
    def _run_rfid(self):
        
        import serial
        
        keyboard = Keyboard(self.experiment, timeout=0)
        s = serial.Serial(self.var.serial_port, timeout=0.01)
        s.flushInput()
        buffer = b''
        while True:
            # Also accept key presses as RFIDs for testing.
            key, _ = keyboard.get_key()
            if key:
                rfid = key
                break
            # Read at most RFID_LENGTH bytes from the serial port. This can
            # also result in fewer bytes.
            buffer += s.read(RFID_LENGTH)
            # Split the buffer based on the RFID separator byte, and keep only
            # those elements that have the expected length, in case the buffer
            # contains some fragments of RFIDs.
            rfids = [
                rfid for rfid in buffer.split(RFID_SEP)
                if len(rfid) == RFID_LENGTH
            ]
            # If there more than one different RFIDs, then something went wrong
            # and we reset the buffer.
            if len(set(rfids)) > 1:
                oslogger.warning('inconsistent rfids')
                buffer = b''
                continue
            # If we have the minimum of repetitions of the RFID, then we are
            # satisfied and return the first RFID.
            if len(rfids) >= MIN_REP:
                rfid = safe_decode(rfids[0])
                break
        oslogger.warning('rfid detected: {}'.format(rfid))
        s.close()
        self.experiment.var.set(
            self.var.participant_variable,
            '/{}/'.format(rfid)  # Flank with / to make sure it's a string
        )
    
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
