"""Manage OpenMonkeyMind experiments"""

label = "OMM Client"
icon = "network-workgroup"
menu = {
  "index": -1,
  "separator_before": True,
  "submenu": "Tools"
}
settings = {
  "omm_server": "127.0.0.1",
  "omm_port": 3000,
  "omm_detector": "form",
  "omm_backend": "psycho",
  "omm_width": 1024,
  "omm_height": 768,
  "omm_fullscreen": False,
  "omm_fallback_experiment": "",
  "omm_local_logfile": "omm.log",
  "omm_yaml_data": ""
}
