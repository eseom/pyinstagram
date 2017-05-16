from __future__ import unicode_literals, print_function

import unittest
import json

from pyinstagram.response import Sync, Challenge
from pyinstagram.response.super import unmarshal


class ResponseTester(unittest.TestCase):
    def test_sync(self):
        data = json.loads(
            '{"experiments": [{"name": "ig_android_sms_consent_in_reg", "group": "launch_0307", "params": [{"name": "show_sms_consent", "value": "true"}]}, {"name": "ig_android_background_conf_resend_fix", "group": "launch", "params": [{"name": "fix_enabled", "value": "true"}]}, {"name": "ig_android_gmail_oauth_in_reg", "group": "test_20161129", "params": [{"name": "try_background_confirm", "value": "true"}]}, {"name": "ig_android_phoneid_sync_interval", "group": "test_6_hours", "params": [{"name": "fully_synced", "value": "604800"}, {"name": "partially_synced", "value": "21600"}]}, {"name": "ig_android_non_fb_sso", "group": "test_20160629", "params": [{"name": "support_non_fb_sso", "value": "true"}]}, {"name": "ig_android_family_apps_user_values_provider_universe", "group": "test", "params": [{"name": "should_provide_user_values", "value": "true"}]}, {"name": "ig_android_background_phone_confirmation_v2", "group": "test_background_confirm_only_1119", "params": [{"name": "background_phone_confirm_enabled", "value": "true"}, {"name": "move_confirmation_screen_to_end_of_phone_flow", "value": "false"}]}, {"name": "ig_android_please_create_username_universe", "group": "launch", "params": [{"name": "please_create_username_enabled", "value": "true"}]}, {"name": "ig_android_gmail_oauth_in_access", "group": "test_gmail_directly_login_20170307", "params": [{"name": "allow_gmail_oauth", "value": "true"}, {"name": "directly_login", "value": "true"}]}, {"name": "ig_android_reg_whiteout_redesign_v3", "group": "whiteout_grey_nav_links_exclude_sign_up_0306", "params": [{"name": "exclude_login_in_page", "value": "false"}, {"name": "exclude_sign_up_page", "value": "true"}, {"name": "grey_nav_links_instead_of_blue", "value": "true"}, {"name": "show_redesign", "value": "true"}]}], "status": "ok"} ')
        sync = unmarshal(data, Sync)
        self.assertEquals(sync.experiments[0].params[0].name,
                          'show_sms_consent')

    def test_challenge(self):
        data = json.loads('{"status": "ok"}')
        challenge = unmarshal(data, Challenge)
        self.assertEquals(challenge.status, 'ok')
