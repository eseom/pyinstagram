PERSISTENT_KEYS = [
    'account_id',  # The numerical UserPK ID of the account.
    'devicestring',  # Which Android device they're identifying as.
    'device_id',  # Hardware identifier.
    'phone_id',  # Hardware identifier.
    'uuid',  # Universally unique identifier.
    'token',  # CSRF token for the logged in session.
    'advertising_id',  # Google Play advertising ID.
    'last_login',  # Tracks time elapsed since our last login state refresh.
]


class Storage(object):
    def __init__(self):
        self.user_settings = {}

    def open_user(self, username):
        pass

    def close_user(self):
        pass

    def load_user_settings(self):
        return self.user_settings


class Setting(object):
    def __init__(self):
        self.storage = Storage()
        self.username = ''
        self.user_settings = []
        pass

    def set_active_user(self, username):
        if self.username == username:
            return

        if self.username is not None:
            self.storage.close_user()

        self.username = username
        self.user_settings = []
        self.storage.open_user(username)

        for key, val in self.storage.load_user_settings().items():
            if key in PERSISTENT_KEYS:
                self.user_settings[key] = val

