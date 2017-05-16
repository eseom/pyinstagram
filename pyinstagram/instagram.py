from __future__ import unicode_literals, print_function

from . import signature, constants, response
from .client import Client
from .device import Device
from collections import OrderedDict


class Instagram(object):
    def __init__(self, setting):
        self.setting = setting

        self.device = None
        self.username = None
        self.password = None
        self.uuid = None
        self.advertising_id = None
        self.device_id = None

        self.is_logged_in = False
        self.account_id = None
        self.rank_token = None
        self.token = None

        self.client = Client(self)

    def set_user(self, username, password):
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
            self.setting.set('device_id', signature.generate_device_id())
            self.setting.set('phone_id', signature.generate_uuid(True))
            self.setting.set('uuid', signature.generate_uuid(True))

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
            self.setting.set('advertising_id', signature.generate_uuid(True))

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

        self.client.update_from_current_settings(reset_cookie_jar)

    def sync_feature(self, pre_login=False):
        if pre_login:
            o = OrderedDict(id=signature.generate_uuid(True),
                            experiments=constants.LOGIN_EXPERIMENTS)
            return self.client.api(
                'qe/sync/', needs_auth=False, data=o,
                response=response.Sync)

    def get_signup_challenge(self):
        return self.client.api(
            'si/fetch_headers/',
            params=OrderedDict(challenge_type='signup',
                               guid=self.uuid.replace('-', '')),
            response=response.Challenge)

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
