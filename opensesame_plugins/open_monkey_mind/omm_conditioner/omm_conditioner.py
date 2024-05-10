from libopensesame.py3compat import *
from . import conditioners
from libopensesame.item import Item
from libopensesame.oslogging import oslogger


class OmmConditioner(Item):

    def reset(self):

        self.var.conditioner = 'Dummy'
        self.var.fallback_conditioner = 'Dummy'
        self.var.serial_port = 'COM4'
        self.var.reward = 'yes'
        self.var.sound = 'do nothing'
        self.var.motor_n_pulses = 5
        self.var.motor_pause = 200
        
    def _init_conditioner(self):
        
        if hasattr(self, '_conditioner'):
            return
        if 'omm_conditioner' in self.python_workspace:
            self._conditioner = self.python_workspace['omm_conditioner']
            oslogger.info('reusing conditioner')
            return
        oslogger.info('initializing conditioner: {}'.format(
            self.var.conditioner))
        cls = getattr(conditioners, self.var.conditioner)
        try:
            self._conditioner = cls(
                experiment=self.experiment,
                port=self.var.serial_port
            )
        except Exception as e:
            oslogger.info(
                'failed to initialize ({}), falling back to: {}'.format(
                    e, self.var.fallback_conditioner))
            cls = getattr(conditioners, self.var.fallback_conditioner)
            self._conditioner = cls(
                experiment=self.experiment,
                port=self.var.serial_port
            )
        self.python_workspace['omm_conditioner'] = self._conditioner
        self.experiment.cleanup_functions.append(self._close_conditioner)
        
    def _close_conditioner(self):
        
        oslogger.info('closing conditioner')
        self._conditioner.close()
        
    def prepare(self):
        
        self._init_conditioner()
        self.experiment.var.omm_conditioner_action = ''
        
    def run(self):

        self.set_item_onset()
        actions = []
        if self.var.reward == 'yes':
            self._conditioner.motor_n_pulses = self.var.motor_n_pulses
            self._conditioner.motor_pause = self.var.motor_pause
            self._conditioner.reward()
            actions.append('reward')
        if self.var.sound == 'do nothing':
            pass
        elif self.var.sound == 'left':
            actions.append('sound_left')
            self._conditioner.sound_left()
        elif self.var.sound == 'right':
            actions.append('sound_right')
            self._conditioner.sound_right()
        elif self.var.sound == 'both':
            actions.append('sound_both')
            self._conditioner.sound_both()
        elif self.var.sound == 'off':
            actions.append('sound_off')
            self._conditioner.sound_off()
        else:
            raise ValueError('invalid sound value: {}'.format(self.var.sound))
        self.experiment.var.omm_conditioner_action = '+'.join(actions)
