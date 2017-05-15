from __future__ import unicode_literals, print_function

import json
import os

import shutil

from ...exceptions import SettingsException

SETTINGS_FILE_NAME = '%s-settings.dat'
COOKIES_FILE_NAME = '%s-cookies.dat'
STORAGE_VERSION = 2


def write(settings_file, encoded_data):
    try:
        tmp_file = '%s_tmp' % settings_file
        with open(tmp_file, 'w') as fp:
            fp.write(encoded_data)
            fp.flush()
            os.fsync(fp.fileno())
        os.rename(tmp_file, settings_file)
        return True
    except Exception as e:
        return False


def create_dir(path):
    if os.path.exists(path):
        return
    try:
        os.makedirs(path)
    except:
        raise SettingsException('The "%s" folder is not writable.' % path)


class File(object):
    __slots__ = ['username', 'base_directory', 'settings_file', 'cookies_file']

    def __init__(self):
        self.base_directory = None
        self.username = None
        self.settings_file = None
        self.cookies_file = None

    def set_options(self, options):
        if 'base_directory' not in options.keys():
            raise SettingsException('required base_directory for file handler')
        self.base_directory = options['base_directory']

    def reset(self):
        self.username = None
        self.settings_file = None
        self.cookies_file = None

    def open_user(self, username):
        user_paths = self.generate_user_path(username)
        create_dir(user_paths['user_directory'])
        self.username = username
        self.settings_file = os.path.join(user_paths['user_directory'],
                                          user_paths['settings_file'])
        self.cookies_file = os.path.join(user_paths['cookies_file'],
                                         user_paths['cookies_file'])

    def close_user(self):
        """
        close current user
        """
        self.reset()

    def generate_user_path(self, username):
        user_directory = os.path.join(self.base_directory, username)
        settings_file = SETTINGS_FILE_NAME % username
        cookies_file = COOKIES_FILE_NAME % username

        return {
            'user_directory': user_directory,
            'settings_file': settings_file,
            'cookies_file': cookies_file,
        }

    def load_user_settings(self):
        user_settings = {}
        if not os.path.exists(self.settings_file):
            return user_settings
        with open(self.settings_file) as fp:
            raw_data = fp.read().replace('FILESTORAGEv2;', '')
            user_settings = json.loads(raw_data)
            return user_settings

    def save_user_settings(self, user_settings):
        version_header = 'FILESTORAGEv%s;' % STORAGE_VERSION
        encoded_data = '%s%s' % (version_header, json.dumps(user_settings))
        write(self.settings_file, encoded_data)

    def delete_user(self, username):
        user_to_delete = self.generate_user_path(username)
        if not os.path.exists(user_to_delete['user_directory']):
            return
        shutil.rmtree(user_to_delete['user_directory'])
