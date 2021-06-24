import sys
sys.path.append(
    '/home/sebastiaan/git/omm-client/opensesame_plugins/OMMConditioner'
)

from libopensesame.experiment import experiment
from conditioners import SeedDispenser

exp = experiment(string='')
exp.init_clock()
sd = SeedDispenser(
    experiment=exp,
    port='/dev/ttyUSB0', 
    motor_n_pulses=10,
    motor_pause=1000
)
input('reward')
sd.reward()
input('sound left')
sd.sound_left()
input('off')
sd.sound_off()
input('sound right')
sd.sound_right()
input('off')
sd.sound_off()
input('sound both')
sd.sound_both()
input('off')
sd.sound_off()
