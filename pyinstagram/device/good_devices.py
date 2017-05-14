import random

__DEVICES = [
    '24/7.0; 380dpi; 1080x1920; OnePlus; ONEPLUS A3010; OnePlus3T; qcom',
    '23/6.0.1; 640dpi; 1440x2392; LGE/lge; RS988; h1; h1',
    '24/7.0; 640dpi; 1440x2560; HUAWEI; LON-L29; HWLON; hi3660',
    '23/6.0.1; 640dpi; 1440x2560; ZTE; ZTE A2017U; ailsa_ii; qcom',
    '23/6.0.1; 640dpi; 1440x2560; samsung; SM-G935F; '
    'hero2lte; samsungexynos8890',
    '23/6.0.1; 640dpi; 1440x2560; samsung; SM-G930F; '
    'herolte; samsungexynos8890',
]


def get_random_good_device():
    return __DEVICES[random.randint(0, len(__DEVICES) - 1)]


def is_good_device(device):
    return device in __DEVICES
