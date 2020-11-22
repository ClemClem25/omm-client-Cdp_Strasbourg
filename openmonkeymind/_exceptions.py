# coding=utf-8

from libopensesame.py3compat import *

class NoJobsForParticipant(Exception): pass
class FailedToSendJobResults(Exception): pass
class InvalidJSON(Exception): pass
class FailedToDownloadExperiment(Exception): pass
class FailedToSetJobStates(Exception): pass
class FailedToDeleteJobs(Exception): pass
class FailedToInsertJobs(Exception): pass
class FailedToGetJobs(Exception): pass
