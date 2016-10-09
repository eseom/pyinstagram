import hashlib
import json
import logging
import os

from .constants import API_URL, LOGIN_EXPERIMENTS, EXPERIMENTS
from .response.login import LoginResponse
from .response.logout import LogoutResponse
from .response.sync_features import SyncFeaturesResponse
from .response.user_tags import UserTagsResponse
from .response.v2_inbox import V2InboxResponse
from .session import Session, InstagramException
from .signature import generate_device_id, generate_uuid, generate_signature

try:
    import httplib as http_client
except ImportError:
    import http.client as http_client

# http_client.HTTPConnection.debuglevel = 1

# logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class Instagram(object):
    def __init__(self, username, password, debug=False, ig_data_path=None,
                 truncated_debug=False):
        assert (username)
        assert (password)
        self.request = Session()
        self.debug = debug
        self.is_logged_in = False
        self.username_id = None
        self.rank_token = None
        self.truncated_debug = truncated_debug

        self.username = None
        self.password = None
        self.uuid = None

        h = hashlib.md5()
        h.update(username.encode('utf-8'))
        h.update(password.encode('utf-8'))
        md5 = h.hexdigest()

        self.device_id = generate_device_id(md5)
        self.set_user(username, password)

    def load_login_response(self):
        setting_dir = '/tmp/pyinstagram'
        try:
            os.makedirs(setting_dir)
        except OSError:
            pass
        setting_path = os.path.join(setting_dir, self.username)
        if os.path.exists(setting_path):
            setting = json.load(open(setting_path, 'r'))
            self.request.set_cookies(setting['cookies'])
            del setting['cookies']
            self.is_logged_in = True
            self.username_id = setting['pk']
            self.rank_token = '%s_%s' % (self.username_id, self.uuid)
            return LoginResponse(**setting)

    def save_login_response(self, obj, cookies):
        setting_dir = '/tmp/pyinstagram/%s' % self.username
        obj['cookies'] = cookies
        with open(setting_dir, 'w') as fp:
            json.dump(obj, fp)

    def send(self, url, data=None):
        url = API_URL % url
        data = self.request.send(url=url, data=data)
        if data['status'] != 'ok':
            raise InstagramException(data['message'])
        del data['status']
        return data

    def set_user(self, username, password):
        self.username = username
        self.password = password
        self.uuid = generate_uuid(True)

    def login(self, force=False):
        if not force:
            login_response = self.load_login_response()
            if login_response:
                return login_response

        self.sync_features(True)
        self.send(
            'si/fetch_headers/?challenge_type=signup&guid=%s' %
            generate_uuid(False))

        data = generate_signature(json.dumps({
            'phone_id': generate_uuid(True),
            '_csrftoken': self.request.csrftoken,
            'username': self.username,
            'guid': self.uuid,
            'device_id': self.device_id,
            'password': self.password,
            'login_attempt_count': '0',
        }))
        rv = self.send('accounts/login/', data)

        # save login response
        login = LoginResponse(**rv['logged_in_user'])
        self.save_login_response(rv['logged_in_user'],
                                 self.request.get_cookies())
        self.is_logged_in = True
        self.username_id = login.pk
        self.rank_token = '%s_%s' % (self.username_id, self.uuid)
        return login

    def logout(self):
        logout_response = LogoutResponse(**self.send('accounts/logout/'))
        self.is_logged_in = False
        self.username_id = None
        self.rank_token = None
        return logout_response

    def sync_features(self, prelogin=False):
        if prelogin:
            data = json.dumps(dict(
                id=generate_uuid(True),
                experiments=LOGIN_EXPERIMENTS,
            ))
        else:
            data = json.dumps({
                '_uuid': self.uuid,
                '_uid': self.username_id,
                '_csrftoken': self.request.csrftoken,
                'id': self.username_id,
                'experiments': EXPERIMENTS,
            })
        return SyncFeaturesResponse(
            **self.send('qe/sync/', generate_signature(data)))

    def get_v2_inbox(self):
        return V2InboxResponse(**self.send('direct_v2/inbox/?'))

    def get_user_tags(self):
        return UserTagsResponse(**self.send(
            "usertags/%s/feed/?rank_token=%s&ranked_content=true&" % (
                self.username_id, self.rank_token,)
        ))
