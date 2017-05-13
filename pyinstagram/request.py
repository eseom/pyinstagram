""" request module to instagram """

from __future__ import print_function

import requests
from pyinstagram.constants import get_api_url


def get(path, version=1):
    """GET request"""
    return requests.get(get_api_url(version, path))
