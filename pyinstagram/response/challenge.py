from __future__ import unicode_literals, print_function

from marshmallow import fields
from .super import Response


class Challenge(Response):
    __slots__ = ['status']

    status = fields.Str()
