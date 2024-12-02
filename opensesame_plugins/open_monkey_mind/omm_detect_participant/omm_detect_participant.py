import time
from openexp.keyboard import Keyboard
from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libopensesame import widgets
from libopensesame.item import Item
from openmonkeymind._exceptions import OMMException

RFID_LENGTH = 18    # The number of bytes of an RFID
RFID_SEP = b'\r'    # The byte that separates RFIDs in the buffer


# A dummy class to signal that the RFID monitor crashed
class RFIDMonitorProcessCrashed(OMMException):
    pass


def _rfid_monitor(queue, reset_event, stop_event, port, min_rep=3):
    
    import serial
    print('starting RFID monitor process')
    s = serial.Serial(port, timeout=0.01)
    s.flushInput()
    buffer = b''
    last_rfid = None
    while not stop_event.is_set():
        # When a reset event comes in, we should again accept any new RFID, 
        # which means flushing the input and forgetting the current buffer and
        # last RFID
        if reset_event.is_set():
            print('resetting last rfid')
            reset_event.clear()
            s.flushInput()
            buffer = b''
            last_rfid = None
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
        # and we reset the buffer, keeping only the last RFIDs (keeping 
        # multiple if the buffer ends with multiple repetitions of the same
        # RFID).
        if len(set(rfids)) > 1:
            print(f'inconsistent rfids, only keeping last rfids')
            buffer = RFID_SEP.join([rfids[-1]] * rfids.count(rfids[-1]))
            continue
        # If we have the minimum of repetitions of the RFID, then we are
        # satisfied and take the first RFID. If this RFID is different from
        # the last RFID, we put it onto the queue.
        if len(rfids) >= min_rep:
            rfid = rfids[0].decode()
            if rfid != last_rfid:
                print('rfid detected: {}'.format(rfid))
                queue.put(rfid)
                last_rfid = rfid
    s.close()


class OmmDetectParticipant(Item):
    
    def reset(self):
        
        self.var.detector = 'form'
        self.var.serial_port = 'COM3'
        self.var.participant_variable = 'participant'
        self.var.min_rep = 1
        
    def _prepare_form(self):
        
        self._form = widgets.form(
            self.experiment,
            cols=(1),
            rows=(1, 5),
            item=self,
            clicks=self.var.form_clicks == u'yes'
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
        
        if not hasattr(self.experiment, '_omm_participant_process'):
            oslogger.info('starting RFID monitor process')
            import multiprocessing
            import queue
            self.experiment._omm_participant_queue = multiprocessing.Queue()
            self.experiment._omm_participant_reset_event = multiprocessing.Event()
            self.experiment._omm_participant_stop_event = multiprocessing.Event()
            self.experiment._omm_participant_process = multiprocessing.Process(
                target=_rfid_monitor,
                args=(self.experiment._omm_participant_queue,
                      self.experiment._omm_participant_reset_event,
                      self.experiment._omm_participant_stop_event,
                      self.var.serial_port,
                      self.var.min_rep)
            )
            self.experiment._omm_participant_process.start()
            self.experiment.cleanup_functions.append(self._close_rfid)
        self.run = self._run_rfid
        self._keyboard = Keyboard(self.experiment, timeout=0)
    
    def _run_rfid(self):

        # Reset the monitor so that it accepts any RFID, not only new ones
        self.experiment._omm_participant_reset_event.set()
        # Eat up any pending RFIDs on the queue
        while not self.experiment._omm_participant_queue.empty():
            try:
                self.experiment._omm_participant_queue.get_nowait()
            except queue.Empty:
                break
        # Wait for a new RFID. While waiting, we make sure that the process
        # is still alive, and we also poll the keyboard to allow for testing
        # identifications with a key press
        while self.experiment._omm_participant_queue.empty():
            time.sleep(.01)
            if not self.experiment._omm_participant_process.is_alive():
                raise RFIDMonitorProcessCrashed()
            key, timestamp = self._keyboard.get_key()
            if key is not None:
                oslogger.info('identifier by key: {}'.format(key))
                self.experiment.var.set(
                    self.var.participant_variable,
                    '/{}/'.format(key)
                )
                return
        rfid = self.experiment._omm_participant_queue.get()
        self.experiment.var.set(
            self.var.participant_variable,
            '/{}/'.format(rfid)  # Flank with / to make sure it's a string
        )
        
    def _close_rfid(self):
        # Stop the monitor process so the signal isn't blocked on the next 
        # experiment
        oslogger.info('stopping RFID monitor process')
        self.experiment._omm_participant_stop_event.set()
    
    def prepare(self):
        
        if self.var.detector == 'rfid':
            self._prepare_rfid()
        elif self.var.detector == 'keypress':
            self._prepare_keypress()
        elif self.var.detector == 'form':
            self._prepare_form()
        else:
            raise ValueError("detector should be 'Dummy', 'Form' or 'RFID'")
