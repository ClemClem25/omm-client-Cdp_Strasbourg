# coding=utf-8

from libopensesame.py3compat import *

class OMMException(Exception): pass
class ParticipantNotFound(OMMException): pass
class NoJobsForParticipant(OMMException): pass
class FailedToSendJobResults(OMMException): pass
class InvalidJSON(OMMException): pass
class FailedToDownloadExperiment(OMMException): pass
class FailedToSetJobStates(OMMException): pass
class FailedToDeleteJobs(OMMException): pass
class FailedToInsertJobs(OMMException): pass
class FailedToGetJobs(OMMException): pass
class FailedToSetGenericStudyData(OMMException): pass
class FailedToSetGenericParticipantData(OMMException): pass
class FailedToSetGenericSessionData(OMMException): pass
