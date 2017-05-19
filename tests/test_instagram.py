from __future__ import unicode_literals, print_function

import os
import unittest

from pyinstagram.instagram import Instagram
from pyinstagram.response import Sync, Challenge
from pyinstagram.setting import Setting


class InstagramTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Setting.create_instance('file', {
            'base_directory': './sessions'
        })

    @classmethod
    def tearDownClass(cls):
        Setting.instance().delete_user('testuser')
        os.removedirs('./sessions')

    def setUp(self):
        # a new Instagram instance for every test methods
        self.instagram = Instagram(Setting.instance())

    def test_set_user(self):
        self.assertIsNone(self.instagram.username)
        self.instagram.set_user('testuser', 'testpassword')
        self.assertEquals(self.instagram.username, 'testuser')

    def test_sync_feature_pre_login(self):
        self.instagram.set_user('testuser', 'testpassword')
        response = self.instagram.sync_feature(True)
        self.assertIsInstance(response, Sync)

        self.instagram.set_user('testuser', 'testpassword')
        response = self.instagram.get_signup_challenge()
        self.assertIsInstance(response, Challenge)
