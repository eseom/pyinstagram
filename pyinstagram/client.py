from __future__ import unicode_literals, print_function

import httplib
import json
import logging
import os
import random

import requests

import constants
import utils
from .response.super import unmarshal

if os.environ.get('DEBUG'):
    # Debug logging
    httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    req_log = logging.getLogger('requests.packages.urllib3')
    req_log.setLevel(logging.DEBUG)
    req_log.propagate = True


class Client(object):
    def __init__(self, parent):
        self.parent = parent

        self.user_agent = None
        self.cookie_jar = None

    def update_from_current_settings(self, reset_cookie_jar):
        self.user_agent = self.parent.device.user_agent
        self.cookie_jar = None
        self.load_cookie_jar(reset_cookie_jar)

    def load_cookie_jar(self, reset_cookie_jar=False):
        pass

    def api(self, url, params={}, data={}, needs_auth=True, signed_post=True,
            response=None):
        url = constants.get_api_url(1, url)
        headers = {
            'User-Agent': self.user_agent,
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Encoding': constants.ACCEPT_ENCODING,
            'X-IG-Capabilities': constants.X_IG_Capabilities,
            'X-IG-Connection-Type': constants.X_IG_Connection_Type,
            'X-IG-Connection-Speed': '%d%s' %
                                     (random.randint(1000, 3700), 'kbps',),
            'X-FB-HTTP-Engine': constants.X_FB_HTTP_Engine,
            'Content-Type': constants.CONTENT_TYPE,
            'Accept-Language': constants.ACCEPT_LANGUAGE,
        }

        method = 'get'
        if data:
            method = 'post'

        if signed_post:
            data = utils.generate_signature_for_post(json.dumps(data))

        rv = getattr(requests, method)(url, headers=headers, data=data)

        if rv.status_code != 200:
            raise Exception()

        return unmarshal(json.loads(rv.text), response)
