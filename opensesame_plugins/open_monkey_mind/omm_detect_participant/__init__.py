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
    "label": "Serial ports",
    "name": "line_edit_serial_ports",
    "info": "For RFID readers (comma-separated, e.g. COM3,COM4)",
    "type": "line_edit",
    "var": "serial_ports"
  },
  {
    "label": "Variable",
    "name": "line_edit_participant_variable",
    "info": "To store participant identifier",
    "type": "line_edit",
    "var": "participant_variable"
  },
  {
    "label": "Minimum repetitions",
    "name": "spinbox_min_rep",
    "info": "The number of times the RFID needs to be successfully read",
    "type": "spinbox",
    "var": "min_rep",
    "min_val": 1,
    "max_val": 1000
  }
]

def supports(exp):
    return exp.var.canvas_backend != 'osweb'
