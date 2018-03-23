class Symbol:
    fn = None
    def __init__(self, fn):
        self.fn = fn
        self.__name__ = fn.__name__
        self.__doc__ = fn.__doc__
    def __str__(self):
        return '<Symbol {}>'.format(self.name)
    @property
    def name(self):
        return self.__name__
    @property
    def doc(self):
        return self.__doc__

def make_symbol(sym):
    return sym if isinstance(sym, Symbol) else Symbol(sym)
