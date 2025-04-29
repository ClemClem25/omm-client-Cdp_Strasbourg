import time
from openexp.keyboard import Keyboard
from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libopensesame import widgets
from libopensesame.item import Item
from openmonkeymind._exceptions import OMMException
import multiprocessing
import serial
import queue

RFID_LENGTH = 18    # The number of bytes of an RFID
RFID_SEP = b'\r'    # The byte that separates RFIDs in the buffer

# A dummy class to signal that the RFID monitor crashed
class RFIDMonitorProcessCrashed(OMMException):
    pass

def _rfid_monitor(queue, reset_event, stop_event, ports, min_rep=3):
    print('starting RFID monitor process')
    readers = []
    for port in ports:
        s = serial.Serial(port, timeout=0.01)
        s.flushInput()
        readers.append((port, s))

    buffers = {port: b'' for port, _ in readers}
    last_rfids = {port: None for port, _ in readers}

    while not stop_event.is_set():
        if reset_event.is_set():
            print('resetting RFID readers')
            reset_event.clear()
            for port, reader in readers:
                reader.flushInput()
                buffers[port] = b''
                last_rfids[port] = None

        for port, reader in readers:
            buffers[port] += reader.read(RFID_LENGTH)
            rfids = [
                rfid for rfid in buffers[port].split(RFID_SEP)
                if len(rfid) == RFID_LENGTH
            ]
            if len(set(rfids)) > 1:
                print(f'inconsistent rfids on {port}, only keeping last rfids')
                buffers[port] = RFID_SEP.join([rfids[-1]] * rfids.count(rfids[-1]))
                continue
            if len(rfids) >= min_rep:
                rfid = rfids[0].decode()
                if rfid != last_rfids[port]:
                    print('rfid detected on {}: {}'.format(port, rfid))
                    queue.put((port, rfid))
                    last_rfids[port] = rfid

    for _, reader in readers:
        reader.close()

class OmmDetectParticipant(Item):

    def reset(self):
        self.var.detector = 'form'
        self.var.serial_ports = 'COM3,COM4'  # Multiple ports comma-separated
        self.var.participant_variable = 'participant'
        self.var.min_rep = 1
        self.var.enable_duration = 'no'
        self.var.read_duration = 0

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
            self.experiment._omm_participant_queue = multiprocessing.Queue()
            self.experiment._omm_participant_reset_event = multiprocessing.Event()
            self.experiment._omm_participant_stop_event = multiprocessing.Event()

            ports = [p.strip() for p in self.var.serial_ports.split(',')]

            self.experiment._omm_participant_process = multiprocessing.Process(
                target=_rfid_monitor,
                args=(
                    self.experiment._omm_participant_queue,
                    self.experiment._omm_participant_reset_event,
                    self.experiment._omm_participant_stop_event,
                    ports,
                    self.var.min_rep
                )
            )
            self.experiment._omm_participant_process.start()
            self.experiment.cleanup_functions.append(self._close_rfid)

        self.run = self._run_rfid
        self._keyboard = Keyboard(self.experiment, timeout=0)

    def _run_rfid(self):
        self.experiment._omm_participant_reset_event.set()

        while not self.experiment._omm_participant_queue.empty():
            try:
                self.experiment._omm_participant_queue.get_nowait()
            except queue.Empty:
                break

        start_time = time.time()
        duration_enabled = self.var.get('enable_duration', 'no') == 'yes'
        read_duration = float(self.var.get('read_duration', 0))

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
            if duration_enabled and (time.time() - start_time) > read_duration:
                oslogger.info('Read duration expired, no RFID detected.')
                return

        rfid_data = self.experiment._omm_participant_queue.get()
        if isinstance(rfid_data, tuple):
            port, rfid = rfid_data
            oslogger.info('rfid detected from {}: {}'.format(port, rfid))
        else:
            rfid = rfid_data
            oslogger.info('rfid detected: {}'.format(rfid))
        self.experiment.var.set(
            self.var.participant_variable,
            '/{}/'.format(rfid)
        )

    def _close_rfid(self):
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
            raise ValueError("detector should be 'form', 'keypress', or 'rfid'")
