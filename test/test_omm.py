# coding=utf-8

from openmonkeymind import OpenMonkeyMind
from libopensesame.experiment import experiment
import sqlite3
import os
import sys


def test_init():
    
    global omm
    omm = OpenMonkeyMind()
    omm.verbose = True


def test_announce():
    
    exp = omm.announce(os.environ['PARTICIPANT'])
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

    
def test_insert_jobs():
    
    omm.insert_jobs(
        3,
        [
            {"distractor": "new"},
            {"distractor": "new"}
        ]
    )
    

def test_delete_jobs():
    
    omm.delete_jobs(1, 2)

    
def test_set_job_states():
    
    omm.set_job_states(1, 3, omm.FINISHED)
