# OpenMonkeyMind client software

Sebastiaan Mathôt and Daniel Schreij

Copyright 2020 le Centre National de la Recherche (CNRS)


## Requirements

- OpenSesame 3.3
- OpenMonkeyMind server software


## Quick start

- Open `osexp\omm-entry-point.osexp` in OpenSesame and start it.
- Enter a participant number to start a trial.


## Implementing an experiment for OMM

The experiment `osexp\omm-template.osexp` contains the basic structure of an OMM experiment. Most of the action happens in *trial_sequence*. This can be an arbitrary trial sequence, just like you're used to in regular OpenSesame experiments.

Before *trial_sequence*, *OMMRequestCurrentJob* sets the experimental variables. In that sense, it is similar to what the *block_loop* would do in a regular OpenSesame experiment. When the experiment is launched by the OMM entry-point experiment, jobs are retrieved from the OMM server. When the experiment is launched directly (for testing), jobs are retrieved from the table of *test_loop*.

After *trial_sequence*, *OMMSendCurrentJobResults* sends the job data (i.e. experimental variables) to the OMM server, when the experiment is launched by the OMM entry-point experiment. When the experiment is launched directly (for testing), this item does nothing.

Typically (but not necessarily) an OMM experiment consists of a single trial. A participant will often do multiple trials in a row, but this happens by repeatedly announcing the participant and launching the experiment. In other words, repetition is handled at the level of the entry-point experiment.


## License

TODO

Icons are based on emojis designed by OpenMoji – the open-source emoji and icon project. License: CC BY-SA 4.0
