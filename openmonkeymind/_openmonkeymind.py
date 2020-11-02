# coding=utf-8

from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
import os
import time
import tempfile
import requests
import json
from openmonkeymind._baseopenmonkeymind import BaseOpenMonkeyMind, BaseJob
from openmonkeymind._exceptions import (
    NoJobsForParticipant,
    UnknownParticipant,
    FailedToSendJobResults,
    InvalidJSON,
    FailedToSetJobStates,
    FailedToDeleteJobs,
    FailedToInsertJobs,
    FailedToGetJobs
)
from libopensesame.experiment import experiment


class Job(BaseJob):
    
    def __init__(self, json):
        
        self._id = json['id']
        self._data = {
            v['name']: v['pivot']['value']
            for v in json['variables']
        }
        # The pivot field contains the results data. This is not present when
        # we're requesting the current job to be done, in which case we infer
        # that the job is now started.
        if 'pivot' in json and json['pivot']['data'] is not None:
            # The pivot data can contain multiple entries, in case the job was
            # reset and done again. In this case, the field is a list, and we
            # get the last entry from the list.
            if isinstance(json['pivot']['data'], list):
                self._data.update(json['pivot']['data'][-1])
            else:
                self._data.update(json['pivot']['data'])
            self._state = json['pivot']['status_id']
        else:
            self._state = Job.STARTED


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
        self.verbose = False
        if not oslogger.started:
            oslogger.start('omm')
        
    @property
    def current_participant(self):
        
        return self._participant
    
    @property
    def current_experiment(self):
        
        return self._experiment
    
    @property
    def current_job(self):
        
        return self._job_id
        
    def _get(self, url_suffix, on_error, data=None):
        
        oslogger.info('get {}'.format(url_suffix))
        response = requests.get(self._base_url + url_suffix, json=data)
        if not response.ok:
            raise on_error()
        json = response.json()
        if not isinstance(json, dict) or 'data' not in json:
            raise InvalidJSON(safe_decode(json))
        if self.verbose:
            oslogger.info(json)
        return json['data']
        
    def _delete(self, url_suffix, on_error):
        
        oslogger.info('delete {}'.format(url_suffix))
        response = requests.delete(self._base_url + url_suffix)
        if not response.ok:
            raise on_error()
        
    def _cmd(self, desc, fnc, url_suffix, data, on_error):
        
        oslogger.info('{} {}'.format(desc, url_suffix))
        response = fnc(self._base_url + url_suffix, json=data)
        if not response.ok:
            raise on_error(response.text)
    
    def _patch(self, *args):
        
        self._cmd('patch', requests.patch, *args)

    def _put(self, *args):
        
        self._cmd('put', requests.put, *args)
            
    def _post(self, *args):
        
        self._cmd('post', requests.post, *args)

    def _get_osexp(self, json):
        
        for f in json['files']:
            if not f['type'] == 'experiment':
                continue
            path = f['path']
            break
        else:
            raise InvalidJSON(safe_decode(json))
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
        return Job(json)

    def send_current_job_results(self, job_results):
        
        data = {'data': job_results}
        oslogger.info(data)
        self._patch(
            'participants/{}/{}/result'.format(
                self._participant,
                self._job_id
            ),
            data,
            FailedToSendJobResults
        )
        self._job_id = None
        
    def get_current_job_index(self):
        
        json = self._get(
            'participants/{}/{}/currentjob_idx'.format(
                self._participant,
                self._study
            ),
            NoJobsForParticipant
        )
        return json['current_job_index']
        
    def delete_jobs(self, from_index, to_index):
        
        json = self._delete(
            'studies/{}/jobs/{}/{}'.format(
                self._study,
                from_index,
                to_index
            ),
            FailedToDeleteJobs
        )
        self._job_id = None

    def insert_jobs(self, index, jobs):
        
        self._post(
            'studies/{}/jobs'.format(self._study),
            {'at': index, 'jobs': jobs},
            FailedToInsertJobs
        )

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
        self._job_id = None

    def get_jobs(self, from_index, to_index):
        
        json = self._get(
            'participants/{}/{}/jobs'.format(
                self._participant,
                self._study
            ),
            NoJobsForParticipant,
            data={
                'from': from_index,
                'to': to_index,
            }
        )
        oslogger.info(json)
        return [Job(job) for job in json]
