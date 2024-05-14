"""A plugin to detect participants based on an RFID chip"""

category = "OMM Client"
aliases = ['OMMDetectParticipant']
controls = [
  {
    "label": "detector",
    "name": "combobox_detector",
    "type": "combobox",
    "options": [
      "form",
      "keypress",
      "rfid"
    ],
    "var": "detector"
  },
  {
    "label": "Serial port",
    "name": "line_edit_serial_port",
    "info": "For RFID reader",
    "type": "line_edit",
    "var": "serial_port"
  },
  {
    "label": "Variable",
    "name": "line_edit_participant_variable",
    "info": "To store participant identifier",
    "type": "line_edit",
    "var": "participant_variable"
  },
  {
    "label": "Minimum repititions",
    "name": "spinbox_min_rep",
    "info": "The number of times the RFID needs to be sucessfully read",
    "type": "spinbox",
    "var": "min_rep",
    "min_val": 1,
    "max_val": 1000
  }
]


def supports(exp):
    return exp.var.canvas_backend != 'osweb'
