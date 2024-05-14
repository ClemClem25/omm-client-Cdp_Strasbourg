"""A plugin for dispensing rewards"""

category = "OMM Client"
aliases = ['OMMConditioner']
controls = [
  {
    "label": "conditioner",
    "name": "combobox_conditioner",
    "type": "combobox",
    "options": [
      "Dummy",
      "SeedDispenser"
    ],
    "var": "conditioner"
  },
  {
    "label": "Serial port",
    "name": "line_edit_serial_port",
    "info": "For SeedDispenser",
    "type": "line_edit",
    "var": "serial_port"
  },
  {
    "label": "Number of pulses",
    "name": "spinbox_motor_n_pulses",
    "info": "For SeedDispenser",
    "min_val": 0,
    "max_val": 999,
    "type": "spinbox",
    "var": "motor_n_pulses"
  },
  {
    "label": "Pause between pulses",
    "name": "spinbox_motor_pause",
    "info": "For SeedDispenser",
    "min_val": 1,
    "max_val": 9999,
    "type": "spinbox",
    "suffix": " ms",
    "var": "motor_pause"
  },
  {
    "label": "Reward (seeds)",
    "name": "checkbox_reward",
    "type": "checkbox",
    "var": "reward"
  },
  {
    "label": "Sound",
    "name": "combobox_sound",
    "type": "combobox",
    "options": [
      "do nothing",
      "left",
      "right",
      "both",
      "off"
    ],
    "var": "sound"
  }
]


def supports(exp):
    return exp.var.canvas_backend != 'osweb'
