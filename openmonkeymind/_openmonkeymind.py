# coding=utf-8

from libopensesame.py3compat import *


class OpenMonkeyMind(object):
    
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

    def send_current_job_results(self, job_results):
        
        """Sends results for the current job. This also changed the current job
        status to complete. There is now no current job anymore.
        
        Arguments:
        jon_results -- a dict where keys are experimental variables, and values
        are values.
        """
        
        pass
    
    def get_current_job_index(self):
        
        """Returns the index of the current job in the job table."""
        
        pass
    
    def get_jobs(self, from_index, to_index):
        
        """Returns a list of jobs between from_index and to_index, where
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
