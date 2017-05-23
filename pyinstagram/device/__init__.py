""" initialize device and user_agent for client """

from distutils.version import StrictVersion

import good_devices
from pyinstagram.exceptions import DeviceException

REQUIRED_ANDROID_VERSION = '2.2'
USER_AGENT_FORMAT = 'Instagram %s Android (%s/%s; %s; %s; %s; %s; %s; %s; %s)'


class RuntimeException(Exception):
    pass


def version_compare(v1, v2, op=None):
    _map = {
        '<': [-1],
        'lt': [-1],
        '<=': [-1, 0],
        'le': [-1, 0],
        '>': [1],
        'gt': [1],
        '>=': [1, 0],
        'ge': [1, 0],
        '==': [0],
        'eq': [0],
        '!=': [-1, 1],
        'ne': [-1, 1],
        '<>': [-1, 1]
    }
    v1 = StrictVersion(v1)
    v2 = StrictVersion(v2)
    result = cmp(v1, v2)
    if op:
        assert op in _map.keys()
        return result in _map[op]
    return result


class Device(object):
    __slots__ = ['app_version', 'user_locale', 'device_string',
                 'android_version', 'android_release', 'dpi',
                 'resolution', 'manufacturer', 'brand', 'model', 'device',
                 'cpu', 'user_agent', ]

    def __init__(self, app_version, user_locale, device_string='',
                 auto_fallback=True):
        self.app_version = app_version
        self.user_locale = user_locale
        if auto_fallback and \
            (device_string == '' or
                 not good_devices.is_good_device(device_string)):
            device_string = good_devices.get_random_good_device()

        if device_string == '':
            raise DeviceException('Device string is empty.')

        parts = device_string.split('; ')
        if len(parts) != 7:
            raise DeviceException('Device string "%s" does not conform to '
                                  'the required device format.' % device_string)

        android_os = parts[0].split('/', 2)
        if not version_compare(android_os[1], REQUIRED_ANDROID_VERSION, '>='):
            raise DeviceException(
                'Device string "%s" does not meet the minimum '
                'required Android version "%s" for Instagram.' % (
                    device_string, REQUIRED_ANDROID_VERSION,))

        # check the screen resolution
        resolution = parts[2].split('x', 2)
        pixel_count = int(resolution[0]) * int(resolution[1])
        if pixel_count < 2073600:  # 1920x1080.
            raise DeviceException('device string does not meet the '
                                  'minimum resolution of 1920x1080')
        manufacturer_and_brand = parts[3].split('/', 2)

        self.device_string = device_string
        self.android_version = android_os[0]  # "23"
        self.android_release = android_os[1]  # "6.0.1"
        self.dpi = parts[1]
        self.resolution = parts[1]
        self.manufacturer = manufacturer_and_brand[0]
        self.brand = manufacturer_and_brand[1] if len(
            manufacturer_and_brand) > 1 else None
        self.model = parts[4]
        self.device = parts[5]
        self.cpu = parts[6]

        # build our user agent
        self.user_agent = self.build_user_agent()

    def build_user_agent(self):
        manufacturer_with_brand = self.manufacturer
        if self.brand:
            manufacturer_with_brand += '/%s' % self.brand

        return USER_AGENT_FORMAT % (
            self.app_version,
            self.android_version,
            self.android_release,
            self.dpi,
            self.resolution,
            manufacturer_with_brand,
            self.model,
            self.device,
            self.cpu,
            self.user_locale,
        )

    def __str__(self):
        return '<Device: device_string=%s, user_agent=%s>' % (
            self.device_string, self.user_agent,)
