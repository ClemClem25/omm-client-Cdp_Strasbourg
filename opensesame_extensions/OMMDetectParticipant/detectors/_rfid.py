# coding=utf-8

from detectors._base_detector import BaseDetector


class RFID(BaseDetector):
    
    def __init__(self, omm_detector):
        
        BaseDetector.__init__(omm_detector)        
    
    def start(self):
        
        BaseDetector.start(self)
        
    def stop(self):
        
        BaseDetector.stop(self)
