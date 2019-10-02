class OneMoreTime:
    def __init__(self, MyIteratorClass, extra_value=None, *pp, **kw):
        self.myIterator = MyIteratorClass(*pp, **kw)
        self.extra_value = extra_value

