import os

SETTINGS_FILE_NAME = '%s-settings.dat'
COOKIES_FILE_NAME = '%s-cookies.dat'


class File(object):
    __slots__ = ['base_directory', 'settings_file', 'cookies_file']

    def __init__(self):
        self.base_directory = 'sessions'
        self.settings_file = ''
        self.cookies_file = ''

    def open_user(self, username):
        user_paths = self.generate_user_path(username)
        self.settings_file = user_paths['settings']
        self.cookies_file = user_paths['cookies']

    def generate_user_path(self, username):
        user_directory = os.path.join(self.base_directory, username)
        settings_file = SETTINGS_FILE_NAME % username
        cookies_file = COOKIES_FILE_NAME % username

        return {
            'user_directory': user_directory,
            'settings_file': settings_file,
            'cookies_file': cookies_file,
        }
