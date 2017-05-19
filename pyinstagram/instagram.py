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

    Python code
        author EunseokEom <me@eseom.org>
"""

from __future__ import unicode_literals, print_function

from . import utils, constants, response
from .client import Client
from .device import Device
from collections import OrderedDict


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
            self.setting.set('last_login', 0)

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

        if reset_cookie_jar and self.setting.is_maybe_logged_in():
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

    def sync_feature(self, pre_login=False):
        """
        Perform an Instagram "feature synchronization" call.
        :param pre_login:
        :return:
        """
        if pre_login:
            o = OrderedDict(id=utils.generate_uuid(True),
                            experiments=constants.LOGIN_EXPERIMENTS)
            return self.client.api(
                'qe/sync/', needs_auth=False, data=o,
                responseClass=response.Sync)

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
            responseClass=response.Challenge)

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
