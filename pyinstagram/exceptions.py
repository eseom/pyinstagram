"""
exceptions
"""


class ServerMessageThrower(object):
    pass


class InstagramException(Exception):
    pass


class RequestException(InstagramException):
    pass


class AccountDisabledException(RequestException):
    pass


class CheckpointRequiredException(RequestException):
    pass


class EmptyResponseException(RequestException):
    pass


class EndpointException(RequestException):
    pass


class FeedbackRequiredException(RequestException):
    pass


class ForcedPasswordResetException(RequestException):
    pass


class IncorrectPasswordException(RequestException):
    pass


class InternalException(InstagramException):
    pass


class InvalidUserException(RequestException):
    pass


class LoginRequiredException(RequestException):
    pass


class NetworkException(RequestException):
    pass


class SentryBlockException(RequestException):
    pass


class SettingsException(InternalException):
    pass


class ThrottledException(RequestException):
    pass


class UploadFailedException(RequestException):
    pass


class DeviceException(Exception):
    """
    exception on device module
    """
    pass
