# coding=utf-8

from openmonkeymind import OpenMonkeyMind
from libopensesame.experiment import experiment
import sqlite3
import sys

OMM_SERVER_PATH = '/home/sebastiaan/git/omm-server'


def test_init():
    
    global omm
    omm = OpenMonkeyMind()

def test_announce():
    
    conn = sqlite3.connect(OMM_SERVER_PATH + '/database/development.sqlite')
    for (participant,) in conn.cursor().execute(
        'select identifier from participants'
    ):
        print(participant)
        break
    conn.close()
    exp = omm.announce(participant)
    assert(isinstance(exp, experiment))
    
    
def test_request_current_job():
    
    job = omm.request_current_job()
    assert(isinstance(job, dict))

def test_get_current_job_index():
    
    job_index = omm.get_current_job_index()
    assert(isinstance(job_index, int))

def test_send_current_job_results():
    
    results = {
        'response': 'space',
        'response_time': '1000',
        'correct': '1',
    }
    omm.send_current_job_results(results)

def delete_jobs():
    
    n_deleted = omm.delete_jobs(1, 3)
    assert(n_deleted == 2)
