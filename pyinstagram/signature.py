"""
generator methods
"""

from __future__ import unicode_literals, print_function

import hashlib
import hmac
import time
import uuid

from constants import IG_SIG_KEY, SIG_KEY_VERSION

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


def generate_signature_for_post(data):
    return 'ig_sig_key_version=%s&signed_body=%s.%s' % (
        SIG_KEY_VERSION,
        generate_signature(data),
        quote(data)
    )


def generate_signature(data):
    return hmac.new(IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'),
                    hashlib.sha256).hexdigest()


def generate_uuid(nostrip=True):
    """
    generate random uuid
    """
    generated_uuid = str(uuid.uuid4())
    if nostrip:
        return generated_uuid
    else:
        return str(generated_uuid.replace('-', ''))


def generate_device_id():
    m = hashlib.md5()
    m.update(str(time.time()))
    return 'android-' + m.hexdigest()[:16]
