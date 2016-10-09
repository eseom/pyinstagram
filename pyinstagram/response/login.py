from pyinstagram.module.printable import Printable


class LoginResponse(Printable):
    def __init__(self, username, is_verified, allow_contacts_sync,
                 show_feed_biz_conversion_icon, has_anonymous_profile_picture,
                 profile_pic_url,
                 full_name, pk, is_private):
        self.username = username
        self.is_verified = is_verified
        self.allow_contacts_sync = allow_contacts_sync
        self.show_feed_biz_conversion_icon = show_feed_biz_conversion_icon
        self.has_anonymous_profile_picture = has_anonymous_profile_picture
        self.profile_pic_url = profile_pic_url
        self.full_name = full_name
        self.pk = pk
        self.is_private = is_private
