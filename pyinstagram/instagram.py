"""
    Instagram's private API v2 python implementation

    The original project is written by PHP.

    https://github.com/mgp25/Instagram-API

    TERMS OF USE:
      This code is in no way affiliated with, authorized, maintained, sponsored
      or endorsed by Instagram or any of its affiliates or subsidiaries. This is
      an independent and unofficial API. Use at your own risk.
      We do NOT support or tolerate anyone who wants to use this API to send spam
      or commit other online crimes.
      You will NOT use this API for marketing or other abusive purposes (spam,
      botting, harassment, massive bulk messaging...).

    PHP code
        author mgp25: Founder, Reversing, Project Leader <https://github.com/mgp25>
        author SteveJobzniak <https://github.com/SteveJobzniak>

    translated to Python code
        author EunseokEom <me@eseom.org>
"""

from __future__ import unicode_literals, print_function

import hashlib
import logging
import time
from collections import OrderedDict

from . import utils, constants
from .client import Client
from .device import Device

EXPERIMENTS_REFRESH = 7200


class Instagram(object):
    def __init__(self, setting):
        # the account settings storage
        self.setting = setting

        # the Android Device for the currently active user
        self.device = None

        # currently active Instagram username
        self.username = None

        # currently active Instagram password
        self.password = None

        self.uuid = None

        # Google Play Advertising ID.
        # The advertising ID is a unique ID for advertising, provided by Google
        # Play services for use in Google Play apps. Used by Instagram.
        self.advertising_id = None

        # android device id
        self.device_id = None

        # session status
        self.is_logged_in = False

        # numerical UserPK ID of the active user account
        self.account_id = None

        # rank token
        self.rank_token = None

        # CSRF token
        self.token = None

        # api client instance
        self.client = Client(self)

        # experiments
        self.experiments = []

        # logger
        self.logger = logging.getLogger('pyinstagram')
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            stream_handler = logging.StreamHandler()
            self.logger.addHandler(stream_handler)

    def set_log_level(self, level):
        self.logger.setLevel(level)

    def set_user(self, username, password):
        """
        Set the active account for the class instance.
        You can call this multiple times to switch between multiple accounts.

        :param username: string instagram username
        :param password: string instagram password
        :return:
        """
        if not username or not password:
            raise ValueError(
                'you must provide a username and password to set_user()')

        self.setting.set_active_user(username)
        saved_device_string = self.setting.get('devicestring')
        self.device = Device(constants.IG_VERSION, constants.USER_AGENT_LOCALE,
                             saved_device_string)
        ds = self.device.device_string
        if ds != saved_device_string:
            self.setting.set('devicestring', ds)

        # Generate a brand-new device fingerprint if the Device wasn't reused
        # from settings, OR if any of the stored fingerprints are missing.
        # NOTE: The regeneration when our device model changes is to avoid
        # dangerously reusing the "previous phone's" unique hardware IDs.
        # WARNING TO CONTRIBUTORS: Only add new parameter-checks here if they
        # are CRITICALLY important to the particular device. We don't want to
        # frivolously force the users to generate new device IDs constantly.
        reset_cookie_jar = False
        if (saved_device_string != ds or not self.setting.get('uuid') or
                not self.setting.get('phone_id') or
                not self.setting.get('device_id')):
            self.setting.set('device_id', utils.generate_device_id())
            self.setting.set('phone_id', utils.generate_uuid(True))
            self.setting.set('uuid', utils.generate_uuid(True))

            # Clear other params we also need to regenerate for the new device.
            self.setting.set('advertising_id', '')

            # Remove the previous hardware's login details to force a relogin.
            self.setting.set('account_id', '')
            self.setting.set('token', '')
            self.setting.set('last_login', '0')

            # We'll also need to throw out all previous cookies.
            reset_cookie_jar = True

        # Generate other missing values. These are for less critical parameters
        # that don't need to trigger a complete device reset like above. For
        # example, this is good for new parameters that Instagram introduces
        # over time, since those can be added one-by-one over time without
        # needing to wipe/reset the whole device. Just be sure to also add them
        # to the "clear other params" section above so that these are always
        # properly regenerated whenever the user's whole "device" changes.
        if not self.setting.get('advertising_id'):
            self.setting.set('advertising_id', utils.generate_uuid(True))

        self.username = username
        self.password = password
        self.uuid = self.setting.get('uuid')
        self.advertising_id = self.setting.get('advertising_id')
        self.device_id = self.setting.get('device_id')
        self.experiments = self.setting.get_experiments()

        if not reset_cookie_jar and self.setting.is_maybe_logged_in():
            self.is_logged_in = True
            self.account_id = self.setting.get('account_id')
            self.rank_token = '%s_%s' % (self.account_id, self.uuid,)
            self.token = self.setting.get('token')
        else:
            self.is_logged_in = False
            self.account_id = None
            self.rank_token = None
            self.token = None

        # Configures Client for current user AND updates isLoggedIn state
        # if it fails to load the expected cookies from the user's jar.
        # Must be done last here, so that isLoggedIn is properly updated!
        # NOTE: If we generated a new device we start a new cookie jar.
        self.client.update_from_current_settings(reset_cookie_jar)

    def login(self, force_login=False, app_refresh_interval=1800):
        """
        Login to Instagram or automatically resume and refresh previous session.

        WARNING: You MUST run this function EVERY time your script runs!
        It handles automatic session resume and relogin and app session state
        refresh and other absolutely *vital* things that are
        important if you don't want to be banned from Instagram!

        :param force_login:
        :param app_refresh_interval:
        """
        if not self.is_logged_in or force_login:
            self.sync_features(True)
            signup_challenge = self.get_signup_challenge()

            # TODO exception point
            response = self.client.api(
                'accounts/login/', needs_auth=False,
                data={
                    'phone_id': self.setting.get('phone_id'),
                    '_csrftoken': signup_challenge.csrftoken,
                    'username': self.username,
                    'guid': self.uuid,
                    'adid': self.advertising_id,
                    'device_id': self.device_id,
                    'password': self.password,
                    'login_attempt_count': 0,
                })

            self.update_login_state(response)
            self._send_login_flow(True, app_refresh_interval)
            return response
        return self._send_login_flow(False, app_refresh_interval)

    def update_login_state(self, response):
        self.is_logged_in = True
        self.account_id = response.data['logged_in_user']['pk']
        self.setting.set('account_id', self.account_id)
        self.rank_token = '%s_%s' % (self.account_id, self.uuid,)
        self.token = response.csrftoken
        self.setting.set('token', self.token)
        self.setting.set('last_login', str(time.time()))

    def _send_login_flow(self, just_logged_in, app_refresh_interval=1800):
        """
        SUPER IMPORTANT:

        STOP trying to ask us to remove this code section!

        EVERY time the user presses their device's home button to leave the
        app and then comes back to the app, Instagram does ALL of these things
        to refresh its internal app state. We MUST emulate that perfectly,
        otherwise Instagram will silently detect you as a "fake" client
        after a while!

        You can configure the login's $appRefreshInterval in the function
        parameter above, but you should keep it VERY frequent (definitely
        NEVER longer than 6 hours), so that Instagram sees you as a real
        client that keeps quitting and opening their app like a REAL user!

        Otherwise they WILL detect you as a bot and silently BLOCK features
        or even ban you.

        You have been warned.

        :param just_logged_in:
        :param app_refresh_interval:
        """
        if app_refresh_interval > 21600:
            raise ValueError('Instagram\'s app state refresh interval is NOT '
                             'allowed to be higher than 6 hours, and the '
                             'lower the better!')

        if just_logged_in:
            self.sync_features()
            self.get_autocomplete_user_list()
            self.get_reels_tray_feed()
            self.get_recent_recipients()
            self.get_timeline_feed()
            self.get_ranked_recipients()

            self.get_v2_inbox()
            self.get_recent_activity()
            self.get_visual_inbox()

            self.get_explorer()
        else:
            # Act like a real logged in app client refreshing its news timeline.
            # This also lets us detect if we're still logged in with a
            # valid session.
            try:
                self.get_timeline_feed()
                # \InstagramAPI\Exception\LoginRequiredException $e
            except:
                # If our session cookies are expired, we were now told to login,
                # so handle that by running a forced relogin in that case!
                return self.login(True, app_refresh_interval)
            last_login_time = float(self.setting.get('last_login'))
            if last_login_time == None or \
                        time.time() - last_login_time > app_refresh_interval:
                self.setting.set('last_login', str(time.time()))

                self.get_autocomplete_user_list()
                self.get_reels_tray_feed()
                self.get_recent_recipients()
                self.get_megaphone_log()
                self.get_v2_inbox()
                self.get_recent_activity()
                self.get_explorer()

            last_experiments_time = self.setting.get('last_experiments')
            if last_experiments_time == None or \
                    (time.time() - float(
                        last_experiments_time)) > EXPERIMENTS_REFRESH:
                self.setting.set('last_experiments', time.time())
                self.sync_features()

    def sync_features(self, pre_login=False):
        """
        Perform an Instagram "feature synchronization" call.
        :param pre_login:
        :return:
        """
        if pre_login:
            o = OrderedDict(id=utils.generate_uuid(True),
                            experiments=constants.LOGIN_EXPERIMENTS)
            return self.client.api(
                'qe/sync/', data=o,
                response_class=None)
        else:
            o = OrderedDict({
                '_uuid': self.uuid,
                '_uid': self.account_id,
                '_csrftoken': self.token,
                'id': self.account_id,
                'experiments': constants.EXPERIMENTS,
            })
            response = self.client.api(
                'qe/sync/', needs_auth=True, data=o,
                response_class=None)
            self._save_experiments(response)
            return response

    def _save_experiments(self, sync_response):
        experiments = {}
        for exp in sync_response.data['experiments']:
            if not exp['name']:
                continue
            try:
                experiments[exp['name']]
            except:
                experiments[exp['name']] = {}
            if not exp['params']:
                continue
            for p in exp['params']:
                if not p['name']:
                    continue
                experiments[exp['name']][p['name']] = p['value']
        self.experiments = self.setting.set_experiments(experiments)

    def get_signup_challenge(self):
        """
        Signup challenge is used to get _csrftoken in order to make a
        successful login or registration request.

        :return:
        """
        return self.client.api(
            'si/fetch_headers/',
            params=OrderedDict(challenge_type='signup',
                               guid=self.uuid.replace('-', '')),
            response_class=None)

    def get_autocomplete_user_list(self):
        """
        Retrieve list of all friends.
        :return: response.AutoCompleteUserList
        """
        self.client.api(
            'friendships/autocomplete_user_list/',
            params={'version': 2},
            response_class=None)

    def get_reels_tray_feed(self):
        self.client.api(
            'feed/reels_tray/',
            response_class=None)

    def get_recent_recipients(self):
        return self.client.api('direct_share/recent_recipients/')

    def get_timeline_feed(self, max_id=None):
        """
        get your own timeline feed

        :param max_id: null|string next "maximum ID", used for pagination.
        """
        params = {
            'rank_token': self.rank_token,
            'ranked_content': True,
        }
        if max_id:
            params['max_id'] = max_id
        return self.client.api('feed/timeline', params=params)

    def get_ranked_recipients(self):
        """
        get ranked list of recipients.
        """
        return self.client.api('direct_v2/ranked_recipients', params={
            'show_thread': True,
        })

    def get_v2_inbox(self, cursor_id=None):
        """
        get direct inbox messages for your account.
        :param cursor_id:
        """
        params = {}
        if cursor_id:
            params['cursor_id'] = cursor_id
        return self.client.api('direct_v2/inbox/', params=params)

    def get_recent_activity(self):
        """
        get recent activity.
        """
        return self.client.api('news/inbox/', params={
            'activity_module': 'all',
        })

    def get_visual_inbox(self):
        return self.client.api('direct_v2/visual_inbox')

    def get_explorer(self):
        return self.client.api('discover/explore')

    def get_megaphone_log(self):
        md5 = hashlib.md5()
        md5.update(str(time.time()))

        return self.client.api('megaphone/log/', data={
            'type': 'feed_aysf',
            'action': 'seen',
            'reason': '',
            '_uuid': self.uuid,
            'device_id': self.device_id,
            '_csrftoken': self.token,
            'uuid': md5.hexdigest(),
        }, signed_post=False)

    def __str__(self):
        return ('<Instagram: settings=%s, device=%s, username=%s, '
                'uuid=%s, advertising_id=%s, device_id=%s, '
                'is_logged_in=%s, account_id=%s, rank_token=%s, '
                'token=%s, client=%s' % (
                    self.setting,
                    self.device,
                    self.username,
                    self.uuid,
                    self.advertising_id,
                    self.device_id,
                    self.is_logged_in,
                    self.account_id,
                    self.rank_token,
                    self.token,
                    self.client,
                ))
