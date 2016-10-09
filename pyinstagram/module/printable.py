class Printable(object):
    def __repr__(self):
        t = []
        for i in dir(self):
            if i.startswith('__'): continue
            t.append('%s: %s' % (i, getattr(self, i)))
        return '<%s (%s)>' % (self.__class__.__name__, ', '.join(t))
