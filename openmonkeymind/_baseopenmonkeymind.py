# coding=utf-8

from libopensesame.py3compat import *


class BaseJob:
    
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

    def __init__(self):
        
        pass
    
    @property
    def current_participant(self):
        
        pass
    
    @property
    def current_experiment(self):
        
        pass
    
    @property
    def current_job(self):
        
        pass
        
    def announce(self, participant):
        
        """Announces a new participant, and retrieves the experiment file for
        that participant. The returned experiment is now the current
        experiment. The participant is now the current participant.
        
        Arguments:
        participant -- a participant id
        
        Returns:
        An experiment object
        """

        pass
        
    def request_current_job(self):
        
        """Gets the first open job for the current experiment and participant.
        The returned job is now the current job.
        
        Returns:
        A dict with where keys are names of experimental variables, and values
        are values. The optional special key '__inline_script__' allows
        arbitrary Python code to be executed in the workspace of the
        experiment.
        """
        
        pass

    def send_current_job_results(self, job_results):
        
        """Sends results for the current job. This also changed the current job
        status to complete. There is now no current job anymore.
        
        Arguments:
        jon_results -- a dict where keys are experimental variables, and values
        are values.
        """
        
        pass
    
    def get_current_job_index(self):
        
        """Returns the index of the current job in the job table. This reflects
        the order of the job table and is therefore different from the job is
        as provided by the current_job property.
        """
        
        pass
    
    def get_jobs(self, from_index, to_index):
        
        """Returns a list of Job objects between from_index and to_index, where
        to_index is not included (i.e. Python-slice style).
        """
        
        pass
    
    def insert_jobs(self, index, jobs):
        
        """Inserts a list of jobs at the specified index, such that the first
        job in the list has the specified index. There is now no current job
        anymore.
        """
        
        pass
    
    def delete_jobs(self, from_index, to_index):
        
        """Deletes all jobs between from_index and to_index, where to_index is
        not included (i.e. Python-slice style). There is now no current job
        anymore.
        """
        
        pass
    
    def set_job_states(self, from_index, to_index, state):
        
        """Sets the states of all jobs between from_index and to_index, where
        to_index is not included (i.e. Python-slice style). There is now no
        current job anymore.
        
        If a job already had results and is set to open. Then the results are
        not reset. Rather, the job will get a second set of results.
        """
        
        pass

    def __reduce__(self):
        
        """Avoid an error during unpickling."""
        
        return (object, ())
