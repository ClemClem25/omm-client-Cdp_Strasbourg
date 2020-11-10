# OpenMonkeyMind client software

Sebastiaan Mathôt and Daniel Schreij

Copyright 2020 le Centre National de la Recherche (CNRS)

## Jump to

- [Requirements](#requirements)
- [License](#license)
- [Connecting to the OMM Server](#connecting-to-the-omm-server)
- [Implementing an experiment for OMM](#implementing-an-experiment-for-omm)
- [The `omm` Python object](#the-omm-python-object)


## Requirements

- OpenSesame 3.3
- [OpenMonkeyMind server software](https://github.com/open-cogsci/omm-server)


## Installation

You can install OpenMonkeyMind through PyPi/ pip:

```
pip install openmonkeymind
```

Or through Anaconda (if you're running an Anaconda Python environment):

```
conda install openmonkeymind -c cogsci -y
```

To run these commands in the OpenSesame console, you need to prefix them with `!`:

```
!conda install openmonkeymind -c cogsci -y
```


## Connecting to the OMM server

The easiest way to connect to an OMM server is through the OpenMonkeyMind extension (Menu → Tools → OpenMonkeyMind). This opens a basic configuration panel that specifies a few things:

- The __address__ and __port__ of the OMM server. (An OMM server mus be running, either locally on your own computer or somewhere else.)
- The __identification method__ that is used to announce participants.
  - The *keypress* method collects a single key press, which means that participant identifiers are limited to single characters.
  - The *form* method collects a multicharacter identifier through a text-input form.
  - The *rfid* method reads an identifier from an RFID chip (specific to Rousset).
- The __backend__, __display resolution__, and a __fullscreen__ option. These options will apply to all experiments running in the session.
- The green play button starts a session.

You can also open a template to create your own entry-point experiment for connecting to an OMM server. By default, the entry-point experiment first waits until a participant identifier is detected with the `OMMDetectParticipant` item. The `OMMAnnounce` item then sends this identifier to the OMM Server, which returns an experiment file that is subsequently started.


## Implementing an experiment for OMM

The easiest way to build a new OMM-compatible experiment is by first opening the OpenMonkeyMind extension (Menu → Tools → OpenMonkeyMind) and from there opening the template for a new experiment. In this template, most of the action happens in *trial_sequence*. This can be an arbitrary trial sequence, just like you're used to in regular OpenSesame experiments.


### Requesting a job from the OMM server

The `OMMRequestJob` item gets a job from the OMM server. Effectively, this sets an experimental variables for each column from the job table. In that sense, it is similar to what the *block_loop* would do in a regular OpenSesame experiment.

If the job contains the variables `_run` and/ or `_prepare` then those are assumed to contain Python code, which is executed during the Run or Prepare phase of the `OMMRequestJob` item.

By default, the next unfinished job will be retrieved. That is, the job table will be consumed from top to bottom. By checking the box 'Randomly select job from block' you can change this behavior such that the job table is treated as a set of blocks, where the jobs inside each block are consumed in a random order, while the blocks themselves are consumed from top to bottom.

If you want to test the experiment by running it directly (i.e. without being connected to an OMM server), then you can indicate a 'Loop for testing'. In that case, a job will be emulated by randomly selecting a row from the `loop` table.

The following variables are set automatically:

- `omm_job_index` indicates the position of the job in the job table, where the first job is at index 1. If the 'Randomly select job from block' option is activated, this index still indicates the position in the job table, and not the position in which the jobs are actually retrieved.
- `omm_block_index` indicates the current block if 'Randomly select job from block' option is activated. Otherwise it is set to `None`.
- `omm_job_index_in_block` indicates the position of the current job in the current block if 'Randomly select job from block' option is activated. This index increments with every job that is retrieved, and is reset to 1 when a new block starts. If this option is deactivated, it is set to `None`.
- `omm_job_count` indicates the number of jobs in the table.
- `omm_job_id` indicates a unique identifier for the job. This identifier is different from `omm_job_index` because it does not indicate the position of the job in the job table.


### Sending job results to the OMM server

You can use a regular `logger` item to send job results (i.e. experimental variables) to the OMM server. (This works because the entry-point experiment installs a special log backend.) In addition to being sent to the server, the job results are also appended in `json` format to the log file that you have indicated when starting the entry-point experiment.


### Seed dispenser

The `OMMConditioner` item allows for dispensing seed rewards (specific to Rousset).


## The `omm` Python object

<div class="ClassDoc YAMLDoc" id="omm" markdown="1">

# class __omm__

Allows for programmatic interaction with the OpenMonkeyMind server.
Lives as the `omm` object in the Python workspace in OpenSesame
experiments.

<div class="FunctionDoc YAMLDoc" id="omm-announce" markdown="1">

## function __omm\.announce__\(participant\)

Announces a new participant, and retrieves the experiment file for
that participant. The returned experiment is now the current
experiment. The participant is now the current participant.

__Arguments:__

- `participant` -- A participant id
	- Type: str, int

__Returns:__

An experiment object.

</div>

<div class="PropertyDoc YAMLDoc" id="omm-current_job" markdown="1">

## property __omm.current_job__

The id of the current job. (This does not correspond to the position of the job in the job table. For that, see `get_current_job_index()`.)

</div>

<div class="PropertyDoc YAMLDoc" id="omm-current_participant" markdown="1">

## property __omm.current_participant__

The identifier of the currently announced participant.

</div>

<div class="PropertyDoc YAMLDoc" id="omm-current_study" markdown="1">

## property __omm.current_study__

The id of the current study.

</div>

<div class="FunctionDoc YAMLDoc" id="omm-delete_jobs" markdown="1">

## function __omm\.delete\_jobs__\(from\_index, to\_index\)

Deletes all jobs between `from_index` and `to_index`, where `to_index` is not included (i.e. Python-slice style). There is now no current job anymore.

__Arguments:__

- `from_index` -- No description
	- Type: int
- `to_index` -- No description
	- Type: int

</div>

<div class="FunctionDoc YAMLDoc" id="omm-get_current_job_index" markdown="1">

## function __omm\.get\_current\_job\_index__\(\)

No description specified.

__Returns:__

The index of the current job in the job table. (This reflects the order of the job table and is therefore different from the job id as provided by the `current_job` property.)

</div>

<div class="FunctionDoc YAMLDoc" id="omm-get_jobs" markdown="1">

## function __omm\.get\_jobs__\(from\_index, to\_index\)

Gets all jobs between `from_index` and `to_index`, where `to_index` is not included (i.e. Python-slice style). The first job has index 1. This does not change the current job.

__Arguments:__

- `from_index` -- No description
	- Type: int
- `to_index` -- No description
	- Type: int

__Returns:__

A `list` of `Job` objects.

- Type: list

</div>

<div class="FunctionDoc YAMLDoc" id="omm-insert_jobs" markdown="1">

## function __omm\.insert\_jobs__\(index, jobs\)

Inserts a list of jobs at the specified index, such that the first job in the list has the specified index. The first job has index 1. There is now no current job anymore.

__Arguments:__

- `index` -- No description
	- Type: int
- `jobs` -- A `list` of `dict` (not `Job`) objects, where the variables and values are keys and values of the dict.
	- Type: list

</div>

<div class="PropertyDoc YAMLDoc" id="omm-job_count" markdown="1">

## property __omm.job_count__

The number of jobs in the job table.

</div>

<div class="FunctionDoc YAMLDoc" id="omm-request_job" markdown="1">

## function __omm\.request\_job__\(job\_index=None\)

Gets a job for the current experiment and participant, i.e. the
first job with a PENDING or STARTED status. The returned job is now
the current job. The state of the job on the server is set to
STARTED.

__Keywords:__

- `job_index` -- The index of the job to request. If this is None, then the next open job (i.e. the first job a PENDING or STARTED status) is retrieved.
	- Type: int
	- Default: None

__Returns:__

No description

- Type: Job

</div>

<div class="FunctionDoc YAMLDoc" id="omm-send_current_job_results" markdown="1">

## function __omm\.send\_current\_job\_results__\(job\_results\)

Sends results for the current job. This changes the current job status to FINISHED. There is now no current job anymore.

__Arguments:__

- `job_results` -- No description
	- Description: A `dict` where keys are experimental variables, and values are values.
	- Type: dict

</div>

<div class="FunctionDoc YAMLDoc" id="omm-set_job_states" markdown="1">

## function __omm\.set\_job\_states__\(from\_index, to\_index, state\)

Sets the states of all jobs between `from_index` and `to_index`,
where `to_index` is not included (i.e. Python-slice style). The
first job has index 1. There is now no current job anymore.

If a job already had results and is set to open. Then the results
are not reset. Rather, the job will get a second set of results.

__Arguments:__

- `from_index` -- No description
	- Type: int
- `to_index` -- No description
	- Type: int
- `state` -- `Job.PENDING`, `Job.STARTED`, or `Job.FINISHED`.
	- Type: int

</div>

</div>


## License

TODO

Icons are based on emojis designed by OpenMoji – the open-source emoji and icon project. License: CC BY-SA 4.0
