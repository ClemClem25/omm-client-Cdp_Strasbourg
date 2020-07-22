# coding=utf-8

from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
import os
import time
import tempfile
import requests
from openmonkeymind._baseopenmonkeymind import BaseOpenMonkeyMind
from openmonkeymind._exceptions import (
    NoJobsForParticipant,
    UnknownParticipant,
    FailedToSendJobResults,
    InvalidJSON,
    FailedToSetJobStates
)
from libopensesame.experiment import experiment


class OpenMonkeyMind(BaseOpenMonkeyMind):
    
    def __init__(self, server='127.0.0.1', port=3000, api=1):
        
        self._server = server
        self._port = port
        self._api = api
        self._base_url = 'http://{}:{}/api/v{}/'.format(server, port, api)
        self._osexp_url = 'http://{}:{}'.format(server, port)
        self._participant = None
        self._study = None
        self._job_id = None
        self._osexp_cache = {}
        
    @property
    def current_participant(self):
        
        return self._participant
    
    @property
    def current_experiment(self):
        
        return self._experiment
    
    @property
    def current_job(self):
        
        return self._job_id
        
    def _get(self, url_suffix, on_error):
        
        oslogger.info('get {}'.format(url_suffix))
        response = requests.get(self._base_url + url_suffix)
        if not response.ok:
            raise on_error()
        json = response.json()
        if not isinstance(json, dict) or 'data' not in json:
            raise InvalidJSON()
        print(json)
        return json['data']
    
    def _patch(self, url_suffix, data, on_error):
        
        oslogger.info('patch {}'.format(url_suffix))
        response = requests.patch(self._base_url + url_suffix, data)
        if not response.ok:
            raise on_error()

    def _put(self, url_suffix, data, on_error):
        
        oslogger.info('patch {}'.format(url_suffix))
        response = requests.put(self._base_url + url_suffix, data)
        if not response.ok:
            raise on_error()

    def _get_osexp(self, json):
        
        path = json['osexp_path']
        if (
            path not in self._osexp_cache or
            self._osexp_cache[path][0] < time.strptime(
                json['updated_at'],
                '%Y-%m-%d %H:%M:%S'
            )
        ):
            response = requests.get(self._osexp_url + path)
            if not response.ok:
                raise FailedToDownloadExperiment()
            with tempfile.NamedTemporaryFile(delete=False) as fd:
                fd.write(response.content)
            self._osexp_cache[path] = time.gmtime(), fd.name
            oslogger.info('caching {} to {}'.format(path, fd.name))
        oslogger.info('returning cached osexp {}'.format(path))
        self._experiment = experiment(string=self._osexp_cache[path][1])
        return self._experiment
    
    def announce(self, participant):
        
        json = self._get(
            'participants/{}/announce'.format(participant),
            NoJobsForParticipant
        )
        if not json['active']:
            raise NoJobsForParticipant()
        self._participant = participant
        self._study = json['id']
        return self._get_osexp(json)
        
    def request_current_job(self):
        
        json = self._get(
            'participants/{}/{}/currentjob'.format(
                self._participant,
                self._study
            ),
            NoJobsForParticipant
        )
        self._job_id = json['id']
        return {v['name']: v['value'] for v in json['variables']}

    def send_current_job_results(self, job_results):
        
        self._patch(
            'participants/{}/{}/result'.format(
                self._participant,
                self._job_id
            ),
            job_results,
            FailedToSendJobResults
        )
        
    def get_current_job_index(self):
        
        json = self._get(
            'participants/{}/{}/currentjob_idx'.format(
                self._participant,
                self._study
            ),
            NoJobsForParticipant
        )
        return json['current_job_index']

    def get_jobs(self, from_index, to_index):
        
        pass
    
    def insert_jobs(self, index, jobs):

        pass
    
    def delete_jobs(self, from_index, to_index):
        
        pass
    
    def set_job_states(self, from_index, to_index, state):
        
        self._put(
            'studies/{}/jobs/state'.format(self._study),
            {
                'from': from_index,
                'to': to_index,
                'state': state,
                'participant': self._participant
            },
            FailedToSetJobStates
        )
