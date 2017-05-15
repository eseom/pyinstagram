from __future__ import print_function

import unittest

from pyinstagram.setting import Setting

from pyinstagram import constants


class SettingTester(unittest.TestCase):
    def test_new_setting(self):
        setting = Setting()
