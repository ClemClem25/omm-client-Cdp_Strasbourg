# coding=utf-8

import multiprocessing
from qtpy.QtCore import QTimer
from detectors._base_detector import BaseDetector


DEFAULT_PORT = 'COM5'


def _read_rfid(queue, port, wait_for_entering=True):

    import serial
    s = serial.Serial(port, timeout=0.1)
    s.flushInput()
    while True:
        rfid = s.read(19)
        if wait_for_entering and rfid:
            queue.put(rfid.decode())
            break
        if not wait_for_entering and not rfid:
            queue.put('leaving')
            break
    s.close()


class RFID(BaseDetector):
    
    def __init__(self, omm_detector, **kwargs):
        
        BaseDetector.__init__(self, omm_detector, **kwargs)
        self._port = kwargs.get('port', DEFAULT_PORT)
    
    def start(self):
        
        BaseDetector.start(self)
        self._queue = multiprocessing.Queue()
        self._process = multiprocessing.Process(
            target=_read_rfid,
            args=(self._queue, self._port, True)
        )
        self._process.start()
        QTimer.singleShot(100, self._poll_start)
        
    def _poll_start(self):
        
        if self._queue.empty():
            QTimer.singleShot(100, self._poll_start)
            return
        self._process.join()
        try:
            self._process.close()
        except AttributeError:
            pass
        self.entering.emit(self._queue.get())
        self.stop()
        
    def stop(self):
        
        BaseDetector.stop(self)
        self._queue = multiprocessing.Queue()
        self._process = multiprocessing.Process(
            target=_read_rfid,
            args=(self._queue, self._port, False)
        )
        self._process.start()
        QTimer.singleShot(100, self._poll_stop)
        
    def _poll_stop(self):
        
        if self._queue.empty():
            QTimer.singleShot(100, self._poll_stop)
            return
        self._process.join()
        try:
            self._process.close()
        except AttributeError:
            pass
        self.leaving.emit()
        self.start()
