"""
test utils
"""

from __future__ import unicode_literals, print_function

import unittest

from pyinstagram.utils import generate_signature_for_post, generate_uuid, \
    generate_device_id


class Tester(unittest.TestCase):
    """
    utils test case
    """

    def test_generate_signature(self):
        """
        test generate_signature function
        """
        src = [['signkey',
                'ig_sig_key_version=4&signed_body=ac6790a5debc0ebac12d89ce3'
                'cff00b581e1189deacdf99239821e17f500b1ec.signkey'],
               ['customkey',
                'ig_sig_key_version=4&signed_body=3dc83e3b2e14375a8cb91e9e0'
                'b5b4373180cef893edf94a74379184d20bfcdf0.customkey']]
        for (sign_key, generated_sign_key) in src:
            self.assertEqual(generate_signature_for_post(sign_key),
                             generated_sign_key)

    def test_generate_uuid(self):
        """
        test generate_uuid function
        """
        uuid = generate_uuid(True)
        self.assertEqual(len(uuid), 36)
        self.assertIsInstance(uuid, str)

        uuid = generate_uuid(False)
        self.assertEqual(len(uuid), 32)
        self.assertIsInstance(uuid, str)

    def test_device_id(self):
        """
        test generate_device_id function
        """
        device_id = generate_device_id()
        self.assertEqual(device_id[0:8], 'android-')
        self.assertEqual(len(device_id), 24)
