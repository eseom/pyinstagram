"""
collection of response data mappers
"""

from collections import namedtuple


SyncResponse = namedtuple('SyncResponse', 'experiments')
ChallengeResponse = namedtuple('ChallengeResponse', 'status')
