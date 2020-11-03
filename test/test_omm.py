# coding=utf-8

from openmonkeymind import OpenMonkeyMind, Job
from openmonkeymind._baseopenmonkeymind import BaseJob
from libopensesame.experiment import experiment
import sqlite3
import os
import sys


class DummyJob(BaseJob):
    
    def __init__(self, id_, state, data):
        
        self._id = id_
        self._state = state
        self._data = data


def init():
    
    global omm
    omm = OpenMonkeyMind()
    omm.verbose = True


def announce():
    
    exp = omm.announce(os.environ['PARTICIPANT'])
    assert(isinstance(exp, experiment))
    
    
def check_jobs(ref_jobs):
    
    act_jobs = omm.get_jobs(1, len(ref_jobs))
    for ref_job, act_job in zip(ref_jobs, act_jobs):
        # We remove the _time and timestamp fields because they're 
        # unpredictable
        if 'timestamp' in act_job:
            del act_job['timestamp']
        if ref_job != act_job:
            raise ValueError('{} != {}'.format(ref_job, act_job))


def clear_jobs():

    # There are two jobs two begin with, but due to the random seeding they
    # sometimes have unpredictable values. So we delete them.
    omm.delete_jobs(1, 3)
    check_jobs([])
    assert(omm.current_job is None)


def insert_jobs():
    
    omm.insert_jobs(
        1,
        [{'distractor': 'absent'}, {'distractor': 'present'}]
    )
    check_jobs([
        DummyJob(3, state=DummyJob.PENDING, data={'distractor': 'absent'}),
        DummyJob(4, state=DummyJob.PENDING, data={'distractor': 'present'})
    ])
    assert(omm.current_job is None)
    
    
def get_first_job():
    
    assert(omm.get_current_job_index() == 1)
    assert(omm.current_job is None)
    cur_job = omm.request_current_job()
    assert(omm.current_job == 3)
    ref_job = DummyJob(
        3,
        state=DummyJob.STARTED,
        data={'distractor': 'absent'}
    )
    if ref_job != cur_job:
        raise ValueError('{} != {}'.format(ref_job, cur_job))
    
    
def send_first_results():

    omm.send_current_job_results({'correct': 1})
    check_jobs([
        DummyJob(
            3,
            state=DummyJob.FINISHED,
            data={'distractor': 'absent', 'correct': 1}
        ),
        DummyJob(
            4,
            state=DummyJob.PENDING,
            data={'distractor': 'present'}
        )
    ])
    assert(omm.current_job is None)


def get_second_job():
    
    assert(omm.get_current_job_index() == 2)
    assert(omm.current_job is None)
    cur_job = omm.request_current_job()
    assert(omm.current_job == 4)
    ref_job = DummyJob(
        4,
        state=DummyJob.STARTED,
        data={'distractor': 'present'}
    )
    if ref_job != cur_job:
        raise ValueError('{} != {}'.format(ref_job, cur_job))


def send_second_results():
    
    omm.send_current_job_results({'correct': 0})
    check_jobs([
        DummyJob(
            3,
            state=DummyJob.FINISHED,
            data={'distractor': 'absent', 'correct': 1}
        ),
        DummyJob(
            4,
            state=DummyJob.FINISHED,
            data={'distractor': 'present', 'correct': 0}
        )
    ])
    assert(omm.current_job is None)
    
    
def reset_jobs():
    
    omm.set_job_states(1, 3, DummyJob.PENDING)
    
    
def skip_to_second_job():
    
    assert(omm.get_current_job_index() == 1)
    assert(omm.current_job is None)
    cur_job = omm.request_job(2)
    assert(omm.current_job == 4)
    ref_job = DummyJob(
        4,
        state=DummyJob.STARTED,
        data={'distractor': 'present', 'correct': 0}
    )
    del cur_job['timestamp']
    if ref_job != cur_job:
        raise ValueError('{} != {}'.format(ref_job, cur_job))


def send_second_results_after_skip():
    
    omm.send_current_job_results({'correct': 1})
    check_jobs([
        DummyJob(
            3,
            state=DummyJob.PENDING,
            data={'distractor': 'absent', 'correct': 1}
        ),
        DummyJob(
            4,
            state=DummyJob.FINISHED,
            data={'distractor': 'present', 'correct': 1}
        )
    ])
    assert(omm.current_job is None)


def test_scenario():
    
    init()
    announce()
    clear_jobs()
    insert_jobs()
    get_first_job()
    send_first_results()
    get_second_job()
    send_second_results()
    reset_jobs()
    get_first_job()
    send_first_results()
    get_second_job()
    send_second_results()
    reset_jobs()
    skip_to_second_job()
    send_second_results_after_skip()


if __name__ == '__main__':
    
    test_scenario()
