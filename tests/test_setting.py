from __future__ import unicode_literals, print_function

import shutil
import unittest

from pyinstagram.exceptions import SettingsException
from pyinstagram.setting import Setting


class SettingTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Setting.create_instance('file', {
            'base_directory': './sessions',
        })

    @classmethod
    def tearDownClass(cls):
        setting = Setting.instance()
        setting.delete_user('test_username')
        shutil.rmtree('./sessions')
        Setting.destroy_instance()

    def test_illegal_way_to_make_instance(self):
        with self.assertRaises(SettingsException):
            Setting()

    def test_new_setting(self):
        setting = Setting.instance()
        setting.set_active_user('test_username')
        self.assertIsNotNone(setting)

    def test_save_setting(self):
        settings = Setting.instance()
        settings.set_active_user('test_username')
        settings.set('account_id', 'test_account_id')
        settings.set('devicestring', 'test_devicestring')

        loaded_settings = settings.load_user_settings()
        self.assertEqual(loaded_settings['account_id'], 'test_account_id')
        self.assertEqual(loaded_settings['devicestring'], 'test_devicestring')

    def test_call_load_user_setting_before_set_active_user(self):
        settings = Setting.instance()
        with self.assertRaises(SettingsException):
            settings.set('some_key', 'some value')

    def test_save_invalid_key(self):
        settings = Setting.instance()
        settings.set_active_user('test_username')
        with self.assertRaises(SettingsException):
            settings.set('invalid_key', 'invalid_value')

    def test_delete_user(self):
        settings = Setting.instance()
        settings.delete_user('test_username')


class NullSettingTester(unittest.TestCase):
    """
    exception when you call instance() before calling create_instance()
    """
    def test_setting_with_no_handler(self):
        with self.assertRaises(SettingsException):
            Setting.instance()


class InvalidSettingTester(unittest.TestCase):
    """
    exception when you call create_instance() with invalid options
    """
    def test_setting_with_invalid_options(self):
        with self.assertRaises(SettingsException):
            Setting.create_instance('file', {})
