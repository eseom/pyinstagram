from __future__ import unicode_literals, print_function

import cookielib
import httplib
import json
import logging
import random
import urllib

import constants
import os
import requests
import utils
from .response.super import unmarshal, Response

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
        self.session = requests.Session()

        self.user_agent = None
        self.cookie_jar = None

        self.last_csrftoken = None

    def update_from_current_settings(self, reset_cookie_jar):
        self.user_agent = self.parent.device.user_agent
        self.cookie_jar = None
        self.load_cookie_jar(reset_cookie_jar)

    def load_cookie_jar(self, reset_cookie_jar=False):
        if reset_cookie_jar:
            self.parent.setting.reset_cookies()
        self.cookie_jar = cookielib.LWPCookieJar(
            self.parent.setting.get_cookies())
        try:
            self.cookie_jar.load()
        except:  # no cookies yet
            pass
        self.session.cookies = self.cookie_jar

    def api(self, url, params=None, data=None, needs_auth=True,
            signed_post=True, response_class=None):
        url = utils.get_api_url(1, url)
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
        if params:
            url = '%s?%s' % (url, urllib.urlencode(params),)

        if data:
            method = 'post'

            if signed_post:
                data = utils.generate_signature_for_post(json.dumps(data))

        self.parent.logger.debug('[%s] %s' % (method.upper(), url,))
        self.parent.logger.debug('sending... %s' % str(data))

        response = getattr(self.session, method)(url, headers=headers,
                                                 data=data)

        if response.status_code != 200:
            raise Exception(response.text)

        loaded_data = json.loads(response.text)
        if response_class:
            response_object = unmarshal(loaded_data, response_class)
        else:
            response_object = Response()
            response_object.data = loaded_data
            self.parent.logger.debug(
                'receiving... %s' % json.dumps(loaded_data, indent=2))
        response_object.full_response = response

        # save cookie
        self.cookie_jar.save(ignore_discard=True)

        # save csrftoken
        for t in iter(self.cookie_jar):
            if t.name == 'csrftoken':
                response_object.csrftoken = t.value
                self.last_csrftoken = t.value
        return response_object
