# coding=utf-8

from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.config import cfg
import detectors


class OMMDetectParticipant(BaseExtension):
    
    def event_startup(self):
        
        self._detector = None
        
    def _init_detector(self):
        
        if self._detector is not None:
            return
        cls = getattr(detectors, cfg.omm_detector_type)
        self._detector = cls(self, port=cfg.omm_detector_serial_port)
        self._detector.entering.connect(self.entering)
        self._detector.leaving.connect(self.leaving)
        oslogger.info('detector initialized')

    def activate(self):
        
        self._init_detector()
        if self._detector.running:
            self._detector.stop()
            oslogger.info('detector stopped')
        else:
            self._detector.start()
            oslogger.info('detector started')

    def entering(self, participant_id):
        
        oslogger.info('participant {} entered'.format(participant_id))
        
    def leaving(self):
        
        oslogger.info('participant left')
        
