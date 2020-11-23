# coding=utf-8

from libopensesame.py3compat import *


class BaseJob:
    
    """A job consists of:
    
    - A state, which can be PENDING, STARTED, or FINISHED
    - An id, which uniquely identifies the job. The id is not an index, that
      is, it does not indicate the position of the job in the job table.
    - A set of job variables, such as experimental conditions.
    - A set of result variables, such as response variables. A job can have
      multiple result variables if the job has been reset and then repeated. In
      that case, the last set of result variables is included.
    """
    
    
    # Job states
    PENDING = 1
    STARTED = 2
    FINISHED = 3
    
    def __init__(self):
        
        self._state = None
        self._id = None
        self._data = {}

    @property
    def state(self):
        
        return self._state
    
    @property
    def id_(self):
        
        return self._id
    
    @property
    def finished(self):
        
        return self._state == BaseJob.FINISHED
    
    @property
    def started(self):
        
        return self._state == BaseJob.STARTED
    
    @property
    def pending(self):
        
        return self._state == BaseJob.PENDING

    def __getitem__(self, key):
        
        return self._data[key]
        
    def __iter__(self):
        
        for key, value in self._data.items():
            yield key, value
                        
    def __eq__(self, other):

        return (
            self.id_ == other.id_ and
            self.state == other.state and
            self._data == other._data
        )
        
    def __str__(self):
        
        return '{}:{}:{}'.format(self.id_, self.state, self._data)
    
    def __repr__(self):
        
        return '{}:{}:{}'.format(self.id_, self.state, self._data)
        
    def __contains__(self, key):
        
        return key in self._data
    
    def __delitem__(self, key):
        
        del self._data[key]


class BaseOpenMonkeyMind(object):
    
    """
    desc: |
        Allows for programmatic interaction with the OpenMonkeyMind server.
        Lives as the `omm` object in the Python workspace in OpenSesame
        experiments.    
    """

    def __init__(self):
        
        self._participant = None
        self._experiment = None
        self._job_id = None
        self._study = None
        self._job_count = None
        self._participant_metadata = {}
    
    @property
    def current_participant(self):
        
        """
        name: current_participant
        desc: The identifier of the currently announced participant.
        """
        
        return self._participant
    
    @property
    def participant_metadata(self):
        
        """
        name: participant_metadata
        desc: A dict with metadata of the participant.
        """
        
        return self._participant_metadata
    
    @property
    def current_study(self):
        
        """
        name: current_study
        desc: The id of the current study.
        """
        
        return self._study
    
    @property
    def current_job(self):
        
        """
        name: current_job
        desc: The id of the current job. (This does not correspond to the
              position of the job in the job table. For that, see
              `get_current_job_index()`.)
        """        
        
        return self._job_id
    
    @property
    def job_count(self):
        
        """
        name: job_count
        desc: The number of jobs in the job table.
        """
        
        return self._job_count
    
    @property
    def connected(self):
        
        """
        name: connected
        desc: "`True` when connected to a server, `False` otherwise."
        """
        
        return self._participant is not None
    
    @property
    def available(self):
        
        """
        name: available
        desc: "`True` when a server appears to be available, `False` otherwise."
        """
        
        raise NotImplementedError()
        
    def announce(self, participant):
        
        """
        desc: |
            Announces a new participant, and retrieves the experiment file for
            that participant. The returned experiment is now the current
            experiment. The participant is now the current participant.
        
        arguments:
            participant:
                desc: A participant id
                type: [str, int]
        
        returns:
            An experiment object.
        """

        pass

    def request_job(self, job_index=None):
        
        """
        desc: |
            Gets a job for the current experiment and participant, i.e. the
            first job with a PENDING or STARTED status. The returned job is now
            the current job. The state of the job on the server is set to
            STARTED.
        
        keywords:
            job_index:
                desc:
                    The index of the job to request. If this is None, then the
                    next open job (i.e. the first job a PENDING or STARTED
                    status) is retrieved.
                type: int
        
        returns:
            type: Job
        """
        
        pass

    def send_current_job_results(self, job_results):
        
        """
        desc:
            Sends results for the current job. This changes the current job
            status to FINISHED. There is now no current job anymore.
        
        arguments:
            job_results:
                description:
                    A `dict` where keys are experimental variables, and values
                    are values.
                type: dict
                
        """
        
        pass
    
    def get_current_job_index(self):
        
        """
        returns:
            The index of the current job in the job table. (This reflects the
            order of the job table and is therefore different from the job id
            as provided by the `current_job` property.)
        """
        
        pass
    
    def get_jobs(self, from_index, to_index):
        
        """
        desc:
            Gets all jobs between `from_index` and `to_index`, where `to_index`
            is not included (i.e. Python-slice style). The first job has index
            1. This does not change the current job.
            
        arguments:
            from_index:
                type: int
            to_index:
                type: int
        
        returns:
            desc: A `list` of `Job` objects.
            type: list
        """
        
        pass

    def insert_jobs(self, index, jobs):
        
        """
        desc:
            Inserts a list of jobs at the specified index, such that the first
            job in the list has the specified index. The first job has index 1.
            There is now no current job anymore.
        
        arguments:
            index:
                type: int
            jobs:
                desc:
                    A `list` of `dict` (not `Job`) objects, where the variables
                    and values are keys and values of the dict.
                type: list
        """
        
        pass
    
    def delete_jobs(self, from_index, to_index):
        
        """
        desc:
            Deletes all jobs between `from_index` and `to_index`, where
            `to_index` is not included (i.e. Python-slice style). There is now
            no current job anymore.
            
        arguments:
            from_index:
                type: int
            to_index:
                type: int
        """
        
        pass
    
    def set_job_states(self, from_index, to_index, state):
        
        """
        desc: |
            Sets the states of all jobs between `from_index` and `to_index`,
            where `to_index` is not included (i.e. Python-slice style). The
            first job has index 1. There is now no current job anymore.
        
            If a job already had results and is set to open. Then the results
            are not reset. Rather, the job will get a second set of results.
        
        arguments:
            from_index:
                type: int
            to_index:
                type: int
            state:
                desc: "`Job.PENDING`, `Job.STARTED`, or `Job.FINISHED`."
                type: int
        """
        
        pass

    def __reduce__(self):
        
        """Avoids an error during unpickling."""
        
        return (object, ())
