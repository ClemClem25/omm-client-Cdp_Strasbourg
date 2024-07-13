# OpenMonkeyMind


*Plugins and extension for OpenSesame*

## About

OpenMonkeyMind (OMM) allows OpenSesame experiments to be managed on a central server ([omm-server](https://github.com/open-cogsci/omm-server)) and deployed to computers running OpenSesame with the [omm-client](https://github.com/open-cogsci/omm-client) software installed. 


## Credits

© 2020 - 2022:

- Sebastiaan Mathôt (@smathot), University of Groningen, The Netherlands
- Daniel Schreij  (@dschreij)
- Joel Fagot (@joelfagot), CNRS and Aix-Marseille University, France
- Nicolas Claidère (@nclaidiere), CNRS and Aix-Marseille University, France
- Pascal Belin, Aix Marseille University, France

The development of Open Monkey Mind was supported by ERC Advanced grant COVOPRIM #78824


## Jump to

- [Requirements](#requirements)
- [Installation](#installation)
- [Connecting to the OMM Server](#connecting-to-the-omm-server)
- [Implementing an experiment for OMM](#implementing-an-experiment-for-omm)
- [The `omm` Python object](#the-omm-python-object)
- [License](#license)


## Requirements

- [OpenSesame 3.3](https://osdoc.cogsci.nl/)
- [OpenMonkeyMind server software](https://github.com/open-cogsci/omm-server)


## Installation

You can install OpenMonkeyMind through PyPi/ pip:

```
pip install opensesame-extension-omm
```

Or through Anaconda (if you're running an Anaconda Python environment):

```
conda install opensesame-extension-omm -c cogsci -y
```

To run these commands in the OpenSesame console, you need to prefix them with `!`:

```
!conda install opensesame-extension-omm -c cogsci -y
```

Ubuntu users can also install OpenMonkeyMind through the Rapunzel PPA:

```
sudo add-apt-repository ppa:smathot/rapunzel
sudo apt update
sudo apt install python3-opensesame-extension-omm
```

## Connecting to the OMM server

The easiest way to connect to an OMM server is through the OpenMonkeyMind extension (Menu → Tools → OpenMonkeyMind). This opens a basic configuration panel that specifies a few things:

- The __Server address__ and __port__ of the OMM server. An OMM server must be running, either locally on your own computer or somewhere else. If a server is detected, the checkmark next to the port will turn green.
- The __identification method__ that is used to announce participants.
  - The *keypress* method collects a single key press, which means that participant identifiers are limited to single characters.
  - The *form* method collects a multicharacter identifier through a text-input form.
  - The *rfid* method reads an identifier from an RFID chip (specific to Rousset).
- The __backend__, __display resolution__, and a __fullscreen__ option. These options will apply to all experiments running in the session.
- The __local log file__ is a file on the local system. Log data will be appended to this log file as one line of JSON data for every time that a `logger` is called. The `logger` also sends this data to the OMM server.
- The __fallback experiment__ is an experiment file on the local system that will be executed when the OMM server cannot be reached or when no jobs are lined up for the participant. The fallback experiment will be disconnected, i.e. the `omm.connected` property will be `False`.
- The __YAML data__ allows you to optionally specify experimental variables in the form of a YAML dictionary.

The green play button starts a session. If the YAML data is invalid or a server is not detected at the specified address and port, the button is disabled.

You can also open a template to create your own entry-point experiment for connecting to an OMM server. By default, the entry-point experiment first waits until a participant identifier is detected with the `OMMDetectParticipant` item. The `OMMAnnounce` item then sends this identifier to the OMM Server, which returns an experiment file that is subsequently started.


## Implementing an experiment for OMM

The easiest way to build a new OMM-compatible experiment is by first opening the OpenMonkeyMind extension (Menu → Tools → OpenMonkeyMind) and from there opening the template for a new experiment. In this template, most of the action happens in *trial_sequence*. This can be an arbitrary trial sequence, just like you're used to in regular OpenSesame experiments.


### Requesting a job from the OMM server

The `OMMRequestJob` item gets a job from the OMM server. Effectively, this sets an experimental variables for each column from the job table. In that sense, it is similar to what the *block_loop* would do in a regular OpenSesame experiment.

If the job contains the variables `_run` and/ or `_prepare` then those are assumed to contain Python code, which is executed during the Run or Prepare phase of the `OMMRequestJob` item.

By default, the next unfinished job will be retrieved. That is, the job table will be consumed from top to bottom. You can also specify a specific job index. This is mostly useful if you want to constrain the order in which jobs are executed.

If you want to test the experiment by running it directly (i.e. without being connected to an OMM server), then you can indicate a 'Loop for testing'. In that case, a job will be emulated by randomly selecting a row from the `loop` table.

The following variables are set automatically:

- `omm_job_index` indicates the position of the job in the job table, where the first job is at index 1.
- `omm_job_count` indicates the number of jobs in the table.
- `omm_job_id` indicates a unique identifier for the job. This identifier is different from `omm_job_index` because it does not indicate the position of the job in the job table.


### Sending job results to the OMM server

You can use a regular `logger` item to send job results (i.e. experimental variables) to the OMM server. (This works because the entry-point experiment installs a special log backend.) In addition to being sent to the server, the job results are also appended in `json` format to the log file that you have indicated when starting the entry-point experiment.


### Seed dispenser

The `OMMConditioner` item allows for dispensing seed rewards (specific to Rousset).


## The `omm` Python object

The `omm` object is added to the Python workspace automatically when an experiment is executed by an entry point; in this case the `omm.connected` property is `True`. Otherwise, the `omm` object is added to the workspace during the prepare phase of the first OMM plug-in in the experiment; in this case, the `omm.connected` property is `False`. Therefore, if you want to use the `omm` object in an `inline_script`, the safest way to do this is to check whether it exists and is connected, like so:

~~~python
if 'omm' in globals() and omm.connected:
    print('Connected to an OMM server')
else:
    print('Not connected to an OMM server')
~~~

<span class="ClassDoc YAMLDoc" id="omm" markdown="1">

# class __omm__

Allows for programmatic interaction with the OpenMonkeyMind server.
Lives as the `omm` object in the Python workspace in OpenSesame
experiments.

<span class="FunctionDoc YAMLDoc" id="omm-announce" markdown="1">

## function __omm\.announce__\(participant\)

Announces a new participant, and retrieves the experiment file for
that participant. The returned experiment is now the current
experiment. The participant is now the current participant.

__Arguments:__

- `participant` -- A participant id
	- Type: str, int

__Returns:__

An experiment object.

</span>

[omm.announce]: #omm-announce
[announce]: #omm-announce

<span class="PropertyDoc YAMLDoc" id="omm-available" markdown="1">

## property __omm.available__

`True` when a server appears to be available, `False` otherwise.

</span>

[omm.available]: #omm-available
[available]: #omm-available

<span class="PropertyDoc YAMLDoc" id="omm-connected" markdown="1">

## property __omm.connected__

`True` when connected to a server, `False` otherwise.

</span>

[omm.connected]: #omm-connected
[connected]: #omm-connected

<span class="PropertyDoc YAMLDoc" id="omm-current_job" markdown="1">

## property __omm.current_job__

The id of the current job. (This does not correspond to the position of the job in the job table. For that, see `get_current_job_index()`.)

</span>

[omm.current_job]: #omm-current_job
[current_job]: #omm-current_job

<span class="PropertyDoc YAMLDoc" id="omm-current_participant" markdown="1">

## property __omm.current_participant__

The identifier of the currently announced participant.

</span>

<span class="PropertyDoc YAMLDoc" id="omm-current_participant_changed" markdown="1">

## property __omm.current_participant_changed__

Indicates whether a new participant identifier is available. If
this is true, the current participant is not automatically changed.
Rather, this property allows the system to check whether a new
participant would be identified if we would detect again.

</span>

[omm.current_participant]: #omm-current_participant
[current_participant]: #omm-current_participant

<span class="PropertyDoc YAMLDoc" id="omm-current_participant_name" markdown="1">

## property __omm.current_participant_name__

The name of the currently announced participant.

</span>

[omm.current_participant_name]: #omm-current_participant_name
[current_participant_name]: #omm-current_participant_name

<span class="PropertyDoc YAMLDoc" id="omm-current_study" markdown="1">

## property __omm.current_study__

The id of the current study.

</span>

[omm.current_study]: #omm-current_study
[current_study]: #omm-current_study

<span class="FunctionDoc YAMLDoc" id="omm-delete_jobs" markdown="1">

## function __omm\.delete\_jobs__\(from\_index, to\_index\)

Deletes all jobs between `from_index` and `to_index`, where `to_index` is not included (i.e. Python-slice style). There is now no current job anymore.

__Arguments:__

- `from_index` -- No description
	- Type: int
- `to_index` -- No description
	- Type: int

</span>

[omm.delete_jobs]: #omm-delete_jobs
[delete_jobs]: #omm-delete_jobs

<span class="PropertyDoc YAMLDoc" id="omm-generic_participant_data" markdown="1">

## property __omm.generic_participant_data__

General-purpose data that is specific to the current participant,
but shared across all studies. The data can be any object that can
be serialized by JSON. If no data has been set, it has the value
`None`.

</span>

[omm.generic_participant_data]: #omm-generic_participant_data
[generic_participant_data]: #omm-generic_participant_data

<span class="PropertyDoc YAMLDoc" id="omm-generic_session_data" markdown="1">

## property __omm.generic_session_data__

General-purpose data that is specific to the current participant
and study. The data can be any object that can be serialized by
JSON. If no data has been set, it has the value `None`.

</span>

[omm.generic_session_data]: #omm-generic_session_data
[generic_session_data]: #omm-generic_session_data

<span class="PropertyDoc YAMLDoc" id="omm-generic_study_data" markdown="1">

## property __omm.generic_study_data__

General-purpose data that is specific to the current study, but
shared across all participants. The data can be any object that can
be serialized by JSON. If no data has been set, it has the value
`None`.

</span>

[omm.generic_study_data]: #omm-generic_study_data
[generic_study_data]: #omm-generic_study_data

<span class="FunctionDoc YAMLDoc" id="omm-get_current_job_index" markdown="1">

## function __omm\.get\_current\_job\_index__\(\)

No description specified.

__Returns:__

The index of the current job in the job table. (This reflects the order of the job table and is therefore different from the job id as provided by the `current_job` property.)

</span>

[omm.get_current_job_index]: #omm-get_current_job_index
[get_current_job_index]: #omm-get_current_job_index

<span class="FunctionDoc YAMLDoc" id="omm-get_jobs" markdown="1">

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

</span>

[omm.get_jobs]: #omm-get_jobs
[get_jobs]: #omm-get_jobs

<span class="FunctionDoc YAMLDoc" id="omm-insert_jobs" markdown="1">

## function __omm\.insert\_jobs__\(index, jobs\)

Inserts a list of jobs at the specified index, such that the first job in the list has the specified index. The first job has index 1. There is now no current job anymore.

__Arguments:__

- `index` -- No description
	- Type: int
- `jobs` -- A `list` of `dict` (not `Job`) objects, where the variables and values are keys and values of the dict.
	- Type: list

</span>

[omm.insert_jobs]: #omm-insert_jobs
[insert_jobs]: #omm-insert_jobs

<span class="PropertyDoc YAMLDoc" id="omm-job_count" markdown="1">

## property __omm.job_count__

The number of jobs in the job table.

</span>

[omm.job_count]: #omm-job_count
[job_count]: #omm-job_count

<span class="PropertyDoc YAMLDoc" id="omm-participant_metadata" markdown="1">

## property __omm.participant_metadata__

A dict with metadata of the participant.

</span>

[omm.participant_metadata]: #omm-participant_metadata
[participant_metadata]: #omm-participant_metadata

<span class="FunctionDoc YAMLDoc" id="omm-request_job" markdown="1">

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

</span>

[omm.request_job]: #omm-request_job
[request_job]: #omm-request_job

<span class="FunctionDoc YAMLDoc" id="omm-send_current_job_results" markdown="1">

## function __omm\.send\_current\_job\_results__\(job\_results\)

Sends results for the current job. This changes the current job status to FINISHED. There is now no current job anymore.

__Arguments:__

- `job_results` -- No description
	- Description: A `dict` where keys are experimental variables, and values are values.
	- Type: dict

</span>

[omm.send_current_job_results]: #omm-send_current_job_results
[send_current_job_results]: #omm-send_current_job_results

<span class="FunctionDoc YAMLDoc" id="omm-set_job_states" markdown="1">

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

</span>

[omm.set_job_states]: #omm-set_job_states
[set_job_states]: #omm-set_job_states

</span>

[omm]: #omm



## License

Icons are based on emojis designed by OpenMoji – the open-source emoji and icon project. License: CC BY-SA 4.0

The rest of OpenMonkeyMind is distributed under the terms of the GNU General Public License 3. The full license should be included in the file COPYING, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>
