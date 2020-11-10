# coding=utf-8

from libopensesame.py3compat import *
import os
import tempfile
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import BaseExtension


class OpenMonkeyMind(BaseExtension):
    
    preferences_ui = 'extensions.OpenMonkeyMind.openmonkeymind'
    
    def event_startup(self):

        self._widget = None

    def activate(self):
        
        self.tabwidget.add(self.settings_widget(), self.icon(), self.label())

    def settings_widget(self):

        w = super().settings_widget()
        w.ui.button_start.clicked.connect(self._connect)
        w.ui.button_template_entry_point.clicked.connect(
            self._template_entry_point
        )
        w.ui.button_template_experiment.clicked.connect(
            self._template_experiment
        )
        return w

    def _compile_entry_point(self):
        
        with open(self.ext_resource('omm-entry-point.osexp')) as fd:
            script = fd.read()
        script = script.format(
            omm_server=cfg.omm_server,
            omm_port=cfg.omm_port,
            omm_height=cfg.omm_height,
            omm_width=cfg.omm_width,
            omm_detector=cfg.omm_detector,
            canvas_backend=cfg.omm_backend
        )
        fd, path = tempfile.mkstemp(suffix='-omm-entry-point.osexp')
        file = os.fdopen(fd, 'w')
        file.write(script)
        file.close()
        return path
        
    def _connect(self):
        
        self._template_entry_point()
        self.main_window.run_experiment(
            fullscreen=cfg.omm_fullscreen,
            quick=True
        )
    
    def _template_entry_point(self):
        
        path = self._compile_entry_point()
        self.main_window.open_file(path=path, add_to_recent=False)
        os.remove(path)
    
    def _template_experiment(self):
        
        self.main_window.open_file(
            path=self.ext_resource('omm-template.osexp'),
            add_to_recent=False
        )
