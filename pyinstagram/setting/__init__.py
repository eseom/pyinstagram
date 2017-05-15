from __future__ import unicode_literals, print_function

import traceback

from .storages.file import File
from ..exceptions import SettingsException

PERSISTENT_KEYS = [
    'account_id',  # The numerical UserPK ID of the account.
    'devicestring',  # Which Android device they're identifying as.
    'device_id',  # Hardware identifier.
    'phone_id',  # Hardware identifier.
    'uuid',  # Universally unique identifier.
    'token',  # CSRF token for the logged in session.
    'advertising_id',  # Google Play advertising ID.
    'last_login',  # Tracks time elapsed since our last login state refresh.
]


def validate_key(key):
    if key not in PERSISTENT_KEYS:
        raise SettingsException(
            'the settings key "%s" is not a valid persistent key name'
            % key)


class Setting(object):
    __instance = None

    @classmethod
    def create_instance(cls, type, options):
        if cls.__instance:
            raise SettingsException(
                'Setting instance is already exist. call instance()')

        if type == 'file':
            cls.__instance = Setting()
            cls.__instance.set_handler(File(), options)
            return cls.__instance

        raise SettingsException('no such handler type "%s"' % type)

    @classmethod
    def destroy_instance(cls):
        cls.__instance = None

    @classmethod
    def instance(cls):
        if not cls.__instance:
            raise SettingsException(
                'call create_instance() before calling instance()')
        return cls.__instance

    def __init__(self):
        # check singleton
        trace = traceback.format_stack()
        caller = trace[len(trace) - 2]. \
            split(',')[0].replace('File', '').replace('"', '').strip()
        if caller != __file__:
            raise SettingsException(
                'use Setting.instance() instead of Setting() for singleton')

        self.user_settings = []
        self.storage = None

    def set_handler(self, storage, options):
        self.storage = storage
        self.storage.set_options(options)

    def set_active_user(self, username):
        if self.storage.username == username:
            return

        if self.storage.username is not None:
            self.storage.__close_user()

        self.user_settings = {}
        self.storage.open_user(username)

        for key, val in self.storage.load_user_settings().items():
            if key in PERSISTENT_KEYS:
                self.user_settings[key] = val

    def delete_user(self, username):
        self.storage.delete_user(username)

    def load_user_settings(self):
        self.__raise_if_no_active_user()
        return self.storage.load_user_settings()

    def get(self, key):
        self.__raise_if_no_active_user()
        validate_key(key)

        try:
            return self.user_settings[key]
        except:
            return None

    def set(self, key, value=''):
        self.__raise_if_no_active_user()
        validate_key(key)

        if value is None:
            raise SettingsException(
                'illegal attempt to store null value in settings storage')

        value = str(value)
        try:
            if self.user_settings[key] == value:
                return
        except:
            pass
        self.user_settings[key] = value
        self.storage.save_user_settings(self.user_settings)

    def is_maybe_logged_in(self):
        self.__raise_if_no_active_user()
        return (self.storage.has_user_cookies() and
                not self.get('account_id') and
                not self.get('token'))

    def __raise_if_no_active_user(self):
        if self.storage.username is None:
            raise SettingsException('called user-related method before '
                                    'setting the current storage user')

    def __open_user(self, username):
        self.storage.open_user(username)

    def __close_user(self):
        self.__raise_if_no_active_user()
        self.storage.close_user()

    def __str__(self):
        return '<Setting: username=%s, user_settings=%s>' % (
            self.storage.username,
            self.user_settings)
