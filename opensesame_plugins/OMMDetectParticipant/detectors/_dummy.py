# coding=utf-8

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout
from detectors._base_detector import BaseDetector


class DummyDetectorWidget(QWidget):
    
    def __init__(self):
        
        QWidget.__init__(self)
        self.button = QPushButton('Enter')
        self.edit = QLineEdit()
        self.edit.setText('1')
        self._layout = QVBoxLayout()
        self._layout.addWidget(self.button)
        self._layout.addWidget(self.edit)
        self.setLayout(self._layout)
        

class Dummy(BaseDetector):
    
    def __init__(self, omm_detector):
        
        BaseDetector.__init__(self, omm_detector)
        self._widget = DummyDetectorWidget()
        self._widget.button.clicked.connect(self._clicked)
        self._occupied = False
        
    def _clicked(self):
        
        if self._occupied:
            self._widget.button.setText('Enter')
            self._occupied = False
            self.leaving.emit()
            return
        self._occupied = True
        self._widget.button.setText('Leave')
        self.entering.emit(self._widget.edit.text())
    
    def start(self):
        
        BaseDetector.start(self)
        self._widget.show()
        
    def stop(self):
        
        BaseDetector.stop(self)
        self._widget.hide()
