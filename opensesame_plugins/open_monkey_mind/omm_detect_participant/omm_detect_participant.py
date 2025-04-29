import time
import multiprocessing
import serial
import queue
from openexp.keyboard import Keyboard
from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libopensesame import widgets
from libopensesame.item import Item
from openmonkeymind._exceptions import OMMException

RFID_LENGTH = 18  # Number of bytes in a valid RFID
RFID_SEP = b'\r'  # RFID separator in the buffer

# Exception to indicate RFID process crash
class RFIDMonitorProcessCrashed(OMMException):
    pass


def _rfid_monitor(queue, reset_event, stop_event, ports, min_rep=3):
    """
    Modified to support multiple RFID readers (multi-port)
    Each reader has an independent buffer and last seen RFID.
    """
    readers = []
    try:
        for port in ports:
            reader = serial.Serial(port, timeout=0.01)
            reader.flushInput()
            readers.append((port, reader))

        buffers = {port: b'' for port, _ in readers}  # Buffer per port
        last_rfids = {port: None for port, _ in readers}  # Track last RFID per port

        while not stop_event.is_set():
            if reset_event.is_set():
                reset_event.clear()
                for port, reader in readers:
                    reader.flushInput()
                    buffers[port] = b''
                    last_rfids[port] = None

            for port, reader in readers:
                buffers[port] += reader.read(RFID_LENGTH)
                rfids = [r for r in buffers[port].split(RFID_SEP) if len(r) == RFID_LENGTH]

                if len(set(rfids)) > 1:
                    # Inconsistent RFID readings, keep only last consistent entries
                    buffers[port] = RFID_SEP.join([rfids[-1]] * rfids.count(rfids[-1]))
                    continue

                if len(rfids) >= min_rep:
                    rfid = rfids[0].decode()
                    if rfid != last_rfids[port]:
                        queue.put((port, rfid))  # Include port info for traceability
                        last_rfids[port] = rfid

        for _, reader in readers:
            reader.close()

    except Exception as e:
        print(f"Error in RFID monitor: {e}")
        stop_event.set()


class OmmDetectParticipant(Item):

    def reset(self):
        self.var.detector = 'form'
        self.var.serial_ports = 'COM3,COM4'  # Modified: list of serial ports
        self.var.participant_variable = 'participant'
        self.var.min_rep = 1
        self.var.enable_duration = 'no'  # Optional reading timeout control
        self.var.read_duration = 5  # Duration in seconds

    def _prepare_form(self):
        self._form = widgets.form(
            self.experiment,
            cols=(1,),
            rows=(1, 5),
            item=self,
            clicks=self.var.form_clicks == u'yes'
        )
        label = widgets.label(self._form, text='Enter OMM participant identifier')
        self._text_input = widgets.text_input(self._form, return_accepts=True, var=self.var.participant_variable)
        self._form.set_widget(label, (0, 0))
        self._form.set_widget(self._text_input, (0, 1))
        self.run = self._run_form

    def _run_form(self):
        self._form._exec(focus_widget=self._text_input)
        self.experiment.var.set(self.var.participant_variable, '/{}/'.format(self.var.get(self.var.participant_variable)))

    def _prepare_keypress(self):
        self._keyboard = Keyboard(self.experiment)
        self.run = self._run_keypress

    def _run_keypress(self):
        key, timestamp = self._keyboard.get_key()
        oslogger.info('Identifier by key: {}'.format(key))
        self.experiment.var.set(self.var.participant_variable, '/{}/'.format(key))

    def _prepare_rfid(self):
        if not hasattr(self.experiment, '_omm_participant_process'):
            oslogger.info('Starting RFID monitor process')

            self.experiment._omm_participant_queue = multiprocessing.Queue()
            self.experiment._omm_participant_reset_event = multiprocessing.Event()
            self.experiment._omm_participant_stop_event = multiprocessing.Event()

            ports = [p.strip() for p in self.var.serial_ports.split(',')]  # Modified: support multi-port
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

        # Modified: Add support for optional timeout during RFID reading
        duration_enabled = self.var.get('enable_duration', 'no') == 'yes'
        read_duration = float(self.var.get('read_duration', 0))
        start_time = time.time()

        while self.experiment._omm_participant_queue.empty():
            time.sleep(0.01)
            if not self.experiment._omm_participant_process.is_alive():
                raise RFIDMonitorProcessCrashed()

            key, timestamp = self._keyboard.get_key()
            if key is not None:
                oslogger.info('Identifier by key: {}'.format(key))
                self.experiment.var.set(self.var.participant_variable, '/{}/'.format(key))
                return

            if duration_enabled and (time.time() - start_time) > read_duration:
                oslogger.info('Read duration expired, no RFID detected.')
                return

        rfid_data = self.experiment._omm_participant_queue.get()

        if isinstance(rfid_data, tuple) and len(rfid_data) == 2:
            port, rfid = rfid_data  # Modified: extract RFID and port info
            oslogger.info(f'RFID detected from {port}: {rfid}')
        else:
            rfid = rfid_data
            oslogger.info(f'RFID detected (no port info): {rfid}')

        self.experiment.var.set(self.var.participant_variable, '/{}/'.format(rfid))

    def _close_rfid(self):
        oslogger.info('Stopping RFID monitor process')
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
