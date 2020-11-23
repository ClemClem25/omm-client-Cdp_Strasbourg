# coding=utf-8

from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
import os
import time
import tempfile
import hashlib
import requests
import json
from openmonkeymind._baseopenmonkeymind import BaseOpenMonkeyMind, BaseJob
from openmonkeymind._exceptions import (
    NoJobsForParticipant,
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
        if 'pivot' not in json:
            self._state = Job.STARTED
            return
        # The pivot data can contain multiple entries, in case the job was
        # reset and done again. In this case, the field is a list, and we
        # get the last entry from the list.
        if json['pivot']['data'] is not None:
            if isinstance(json['pivot']['data'], list):
                self._data.update(json['pivot']['data'][-1])
            else:
                self._data.update(json['pivot']['data'])
        self._state = json['pivot'].get('status_id', Job.STARTED)


class OpenMonkeyMind(BaseOpenMonkeyMind):

    def __init__(self, server='127.0.0.1', port=3000, api=1):
        
        self._server = server
        self._port = port
        self._api = api
        self._base_url = 'http://{}:{}/api/v{}/'.format(server, port, api)
        self._osexp_url = 'http://{}:{}'.format(server, port)
        self._participant = None
        self._participant_metadata = {}
        self._study = None
        self._job_id = None
        self._job_count = None
        self.verbose = False
        if not oslogger.started:
            oslogger.start('omm')
        
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
            updated_at = f['updated_at']
            size = f['size']
            break
        else:
            raise InvalidJSON(safe_decode(json))
        cache_path = os.path.join(
            tempfile.gettempdir(),
            hashlib.md5(safe_encode(path + updated_at)).hexdigest() + '.osexp'
        )
        # If a cached file that matches in name and size exists, we re-use it. 
        # The file name also includes the updated_at fields, and thus 
        # re-uploading a new experiment with the same size will still refresh 
        # the cache.
        if os.path.exists(cache_path) and os.path.getsize(cache_path) == size:
            oslogger.info('using cached {}'.format(cache_path))
        else:
            response = requests.get(self._osexp_url + path)
            if not response.ok:
                raise FailedToDownloadExperiment()
            with open(cache_path, 'wb') as fd:
                fd.write(response.content)
            oslogger.info('caching {} to {}'.format(path, cache_path))
        self._experiment = experiment(string=cache_path)
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
        self._job_count = json['jobs_count']
        # The participant metadata is optional, and is None if no metadata has 
        # been specified.
        metadata = json['participants'][0]['meta']
        if metadata is None:
            self._participant_metadata = {}
        else:
            self._participant_metadata = metadata
        return self._get_osexp(json)
    
    @property
    def available(self):
        
        oslogger.info('check server at {}'.format('healthz'))
        try:
            response = requests.get(self._base_url + 'healthz')
        except requests.exceptions.ConnectionError:
            return False
        return response.ok
        
    def _request_current_job(self):
        
        json = self._get(
            'participants/{}/{}/currentjob'.format(
                self._participant,
                self._study
            ),
            NoJobsForParticipant
        )
        self._job_id = json['id']
        return Job(json)
        
    def request_job(self, job_index=None):
        
        if job_index is None:
            return self._request_current_job()
        self.set_job_states(job_index, job_index + 1, Job.STARTED)
        (job, ) = self.get_jobs(job_index, job_index + 1)
        self._job_id = job.id_
        return job

    def send_current_job_results(self, job_results):
        
        data = {'data': job_results}
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
        return [Job(job) for job in json]
