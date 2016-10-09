import unittest
from pyinstagram.signature import generate_signature, generate_uuid, \
    generate_device_id


class Tester(unittest.TestCase):
    def test_generate_signature(self):
        src = [['signkey',
                'ig_sig_key_version=4&signed_body=132c669f6844651f5e53f91d'
                'ca7e9ee9cf15d07bdd41f6b289e094e9732d0886.signkey'],
               ['customkey',
                'ig_sig_key_version=4&signed_body=9a79c387ed6a890b3ce82304'
                '93aa64f018c9b633c1e7ebf7bf7c202ab3f41a31.customkey']]
        for (s, d) in src:
            self.assertEqual(generate_signature(s), d)

    def test_generate_uuid(self):
        uuid = generate_uuid(True)
        self.assertEqual(len(uuid), 36)
        self.assertIsInstance(uuid, str)

        uuid = generate_uuid(False)
        self.assertEqual(len(uuid), 32)
        self.assertIsInstance(uuid, str)

    def test_device_id(self):
        src = [['seed1', 'android-9437f3195fc63d10'],
               ['seed2', 'android-96476ba6b1ec5ea3'],
               ['seed3', 'android-48320237e596bc81']]
        for (s, d) in src:
            self.assertEqual(generate_device_id(s), d)
