import unittest

from pyinstagram.response.login import LoginResponse
from pyinstagram.response.user_tags import UserTagsResponse
from pyinstagram.response.v2_inbox import V2InboxResponse


class Tester(unittest.TestCase):
    def test_login_response(self):
        # 'logged_in_user':
        LoginResponse(**{
            'is_verified': False,
            'full_name': 'FullName',
            'pk': 3031209939,
            'has_anonymous_profile_picture': True,
            'username': 'username',
            'allow_contacts_sync': False,
            'is_private': False,
            'profile_pic_url': 'http://scontent-dft4-1.cdninstagram.com/'
                               't51.2995-19/'
                               '12936425_9l7283980022114_1248324159_b.jpg',
            'show_feed_biz_conversion_icon': False
        })

    def test_v2_inbox_response(self):
        response = V2InboxResponse(
            **{'pending_requests_total': 10, 'seq_id': 0,
               'inbox': {'unseen_count': 14, 'has_older': False,
                         'unseen_count_ts': 1476224228930961, 'threads': []},
               'subscription': {
                   'sequence': '389846334552670208',
                   'topic': 'user-ds2-4023210249~2',
                   'url': 'wss://telegraph-ash.instagram.com/rt',
                   'auth': 'user-ds2-4023210249~2:1476192282047:'
                           'f4a7d227cc2eea2b37cdd4d1bb7f222b2da570a5'},
               'pending_requests_users': []})
        self.assertEqual(response.pending_requests_total, 10)
        self.assertIsInstance(response.subscription, dict)

    def test_usertags_response(self):
        response = UserTagsResponse(
            **{'more_available': False, 'auto_load_more_enabled': True,
               'total_count': 0, 'items': [],
               'requires_review': False, 'new_photos': [], 'num_results': 0}
        )
        self.assertFalse(response.more_available)
        self.assertEquals(response.total_count, 0)
