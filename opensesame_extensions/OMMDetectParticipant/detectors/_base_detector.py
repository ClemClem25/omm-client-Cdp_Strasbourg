# coding=utf-8

from qtpy import QtCore


class BaseDetector(QtCore.QObject):
    
    entering = QtCore.Signal(str)
    leaving = QtCore.Signal()
    
    def __init__(self, omm_detector):
        
        QtCore.QObject.__init__(self)
        self._omm_detector = omm_detector
        self._running = False
        
    @property
    def running(self):
        
        return self._running
    
    def start(self):
        self._running = True
        
    
    def stop(self):
        
        self._running = False
