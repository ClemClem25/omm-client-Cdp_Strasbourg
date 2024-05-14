"""A plugin for requesting jobs"""

category = "OMM Client"
aliases = ['OMMRequestJob']
controls = [
  {
    "label": "Loop for testing",
    "name": "line_edit_test_loop",
    "type": "line_edit",
    "info": "Defines variables during development",
    "var": "test_loop"
  },
  {
    "label": "Job index",
    "name": "line_edit_job_index",
    "type": "line_edit",
    "info": "Leave empty to select next pending job",
    "var": "job_index"
  },
  {
    "label": "Overwrite",
    "name": "checkbox_overwrite_existing",
    "type": "checkbox",
    "info": "Overwrite values of existing variables",
    "var": "overwrite"
  }
]


def supports(exp):
    return exp.var.canvas_backend != 'osweb'
