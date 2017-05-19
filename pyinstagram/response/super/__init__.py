from __future__ import unicode_literals, print_function

from marshmallow import Schema as Sc, post_load, fields


class RSchema(Sc):
    @post_load
    def page_load(self, data):
        tobject = self.__class__()
        for k, v in data.items():
            setattr(tobject, k, v)
        return tobject


class Response(RSchema):
    def __init__(self, *arg, **kwargs):
        RSchema.__init__(self, *arg, **kwargs)

        self.full_response = None
        self.csrftoken = None

    def __repr__(self):
        all_fields = vars(self)[str('declared_fields')]
        field_repr = []
        for k, v in all_fields.items():
            if isinstance(v, fields.Field):
                field_repr.append('%s=%s' % (k, getattr(self, k),))
        return '<%s: %s>' % (
            str(self.__class__).strip('<>'), ', '.join(field_repr))


def unmarshal(data, klass):
    result = klass().load(data)
    if hasattr(result, 'errors') and result.errors:
        print('--- error:', result.errors)
    return klass().load(data).data
