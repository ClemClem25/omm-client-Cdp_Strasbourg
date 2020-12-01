# coding=utf-8

from libopensesame.py3compat import *
import os
import tempfile
import textwrap
import yaml
from qtpy.QtWidgets import QFileDialog
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.translate import translation_context
from openmonkeymind import OpenMonkeyMind as OMM
_ = translation_context(u'OpenMonkeyMind', category=u'extension')


class OpenMonkeyMind(BaseExtension):
    
    preferences_ui = 'extensions.OpenMonkeyMind.openmonkeymind'
    
    def event_startup(self):

        self._widget = None

    def activate(self):
        
        self.tabwidget.add(self.settings_widget(), self.icon(), self.label())

    def settings_widget(self):

        self._w = super().settings_widget()
        if isinstance(cfg.omm_yaml_data, str):
            self._w.ui.omm_yaml_data.setPlainText(cfg.omm_yaml_data)
        self._w.ui.omm_yaml_data.textChanged.connect(self._validate)
        self._w.ui.button_start.clicked.connect(self._connect)
        self._w.ui.button_template_entry_point.clicked.connect(
            self._template_entry_point
        )
        self._w.ui.button_template_experiment.clicked.connect(
            self._template_experiment
        )
        self._w.ui.button_fallback_experiment_browse.clicked.connect(
            self._select_fallback_experiment
        )
        self._w.ui.button_local_logfile_browse.clicked.connect(
            self._select_local_logfile
        )
        self._validate()
        return self._w
    
    def event_setting_changed(self, setting, value):
        
        if setting in ('omm_server', 'omm_port'):
            self._validate()
            
    def _select_fallback_experiment(self):
        
        path = QFileDialog.getOpenFileName(
            self.main_window,
            _('Open fallback experiment'),
        )
        if isinstance(path, tuple):
            path = path[0]
        if not path:
            return
        cfg.omm_fallback_experiment = path
        self._w.ui.cfg_omm_fallback_experiment.setText(path)
        
    def _select_local_logfile(self):
        
        path = QFileDialog.getSaveFileName(
            self.main_window,
            _('Select local logfile'),
        )
        if isinstance(path, tuple):
            path = path[0]
        if not path:
            return
        cfg.omm_local_logfile = path
        self._w.ui.cfg_omm_local_logfile.setText(path)

    def _validate(self):
        
        self._w.ui.button_start.setEnabled(True)
        if OMM(server=cfg.omm_server, port=cfg.omm_port).available:
            self._w.ui.label_server_status.setText('✓')
            self._w.ui.label_server_status.setStyleSheet('color:green;')
        else:
            self._w.ui.label_server_status.setText('✕')
            self._w.ui.label_server_status.setStyleSheet('color:red;')
            self._w.ui.button_start.setEnabled(False)
        try:
            yaml_data = yaml.safe_load(self._w.ui.omm_yaml_data.toPlainText())
        except:
            self._w.ui.omm_yaml_data.setStyleSheet('color:red;')
            self._w.ui.button_start.setEnabled(False)
        else:
            self._w.ui.omm_yaml_data.setStyleSheet('')
            cfg.omm_yaml_data = (
                '' if yaml_data is None
                else yaml.safe_dump(yaml_data)
            )

    def _compile_entry_point(self):
        
        with open(self.ext_resource('omm-entry-point.osexp')) as fd:
            script = fd.read()
        script = script.format(
            omm_server=cfg.omm_server,
            omm_port=cfg.omm_port,
            omm_height=cfg.omm_height,
            omm_width=cfg.omm_width,
            omm_detector=cfg.omm_detector,
            omm_yaml_data=textwrap.indent(cfg.omm_yaml_data, prefix='\t'),
            omm_local_logfile=cfg.omm_local_logfile,
            omm_fallback_experiment=cfg.omm_fallback_experiment,
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
