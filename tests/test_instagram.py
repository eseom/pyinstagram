import unittest

from pyinstagram.instagram import Instagram
from pyinstagram.response.sync_features import SyncFeaturesResponse

instagram = Instagram('', '')
instagram.login()


class Tester(unittest.TestCase):
    def test_sync_features_prelogin(self):
        instagram.logout()
        self.assertIsInstance(instagram.sync_features(True),
                              SyncFeaturesResponse)
        instagram.login()

    def test_sync_features(self):
        self.assertIsInstance(instagram.sync_features(), SyncFeaturesResponse)

    def test_get_v2_inbox(self):
        instagram.get_v2_inbox()

    def test_get_user_tags(self):
        instagram.get_user_tags()
