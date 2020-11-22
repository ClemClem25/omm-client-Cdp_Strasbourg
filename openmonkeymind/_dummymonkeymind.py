# coding=utf-8

from libopensesame.py3compat import *
import os
from openmonkeymind._baseopenmonkeymind import BaseOpenMonkeyMind
from openmonkeymind._exceptions import NoJobsForParticipant
from libopensesame.experiment import experiment


class DummyMonkeyMind(BaseOpenMonkeyMind):
    
    def __init__(self):
        
        self._jobs = safe_yaml_load(safe_read(os.path.join(
            os.path.dirname(__file__),
            'data',
            'dummy-jobs.yaml'
        )))
        self._participant = None
        self._experiment = None
        self._job = None

    @property
    def current_participant(self):
        
        return self._participant
    
    @property
    def current_experiment(self):
        
        return self._experiment
    
    @property
    def current_job(self):
        
        return self._job
        
    def announce(self, participant):
        
        self._participant = participant
        if self._participant not in self._jobs:
            raise NoJobsForParticipant(participant)
        if not self._jobs[self._participant][0]['jobs']:
            self._jobs[self._participant].pop(0)
        if not self._jobs[self._participant]:
            raise NoJobsForParticipant(participant) 
        path = self._experiment_path(self._jobs[self._participant][0]['exp'])
        self._experiment = experiment(string=path)
        return self._experiment

    def request_current_job(self):

        if not self._jobs[self._participant][0]['jobs']:
            self._job = None
        else:
            self._job = self._jobs[self._participant][0]['jobs'].pop(0)
        return self._job
        
    def send_current_job_results(self, job_results):
        
        print(job_results)
        
    def _experiment_path(self, exp):
        
        return os.path.join(
            os.path.dirname(__file__),
            '..',
            'osexp',
            exp
        )


if __name__ == '__main__':
    
    dmm = DummyMonkeyMind(e)
    print(dmm.announce(1))
    while True:
        job = dmm.request_current_job()
        if job is None:
            break
        print(job)
        
