from __future__ import unicode_literals, print_function

from marshmallow import fields

from .super import Response


class Param(Response):
    __slots__ = ['name', 'value']

    name = fields.Str()
    value = fields.Str()


class Experiments(Response):
    __slots__ = ['name', 'group', 'params']

    name = fields.Str()
    group = fields.Str()
    params = fields.Nested(Param, many=True)


class Sync(Response):
    __slots__ = ['experiments']

    experiments = fields.Nested(Experiments, many=True)
