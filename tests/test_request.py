"""
test responses
"""

from __future__ import print_function

import json
import unittest

from pyinstagram import request, signature
from pyinstagram.responses import ChallengeResponse


class Tester(unittest.TestCase):
    """
    """
    def test_challenge(self):
        """
        test signup challenge
        """
        uuid = signature.generate_uuid()
        print('si/fetch_headers?challenge_type=signup&guid=%s' % uuid.replace('-', ''))
        response = request.get('si/fetch_headers?challenge_type=signup&guid=%s' %
                               uuid.replace('-', ''))
        data = json.loads(response.text)
        response_object = ChallengeResponse(**data)

        print(response.headers)
        print(response_object)
