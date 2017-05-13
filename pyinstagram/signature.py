"""
generate signagures
"""

import uuid


def generate_uuid(type=True):
    """
    generate random uuid
    """
    generated_uuid = str(uuid.uuid4())
    if type:
        return generated_uuid
    else:
        return generated_uuid.replace('-', '')
