from __future__ import print_function

import unittest

from pyinstagram.device import Device

from pyinstagram import constants


class Tester(unittest.TestCase):
    def test_new_device(self):
        device = Device(constants.IG_VERSION, constants.USER_AGENT_LOCALE, '')
        self.assertIsNotNone(device.device_string)
        self.assertNotEquals(device.device_string, '')
        self.assertIsNotNone(device.user_agent)
        self.assertNotEquals(device.user_agent, '')
