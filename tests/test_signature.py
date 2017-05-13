"""
test signature
"""

import unittest

from pyinstagram.signature import generate_signature, generate_uuid, \
    generate_device_id


class Tester(unittest.TestCase):
    """
    signature test case
    """
    def test_generate_signature(self):
        """
        test generate_signature function
        """
        src = [['signkey',
                'ig_sig_key_version=4&signed_body=132c669f6844651f5e53f91d'
                'ca7e9ee9cf15d07bdd41f6b289e094e9732d0886.signkey'],
               ['customkey',
                'ig_sig_key_version=4&signed_body=9a79c387ed6a890b3ce82304'
                '93aa64f018c9b633c1e7ebf7bf7c202ab3f41a31.customkey']]
        for (sign_key, generated_sign_key) in src:
            self.assertEqual(generate_signature(sign_key), generated_sign_key)

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
        src = [['seed1', 'android-9437f3195fc63d10'],
               ['seed2', 'android-96476ba6b1ec5ea3'],
               ['seed3', 'android-48320237e596bc81']]
        for (seed, device_id) in src:
            self.assertEqual(generate_device_id(seed), device_id)
