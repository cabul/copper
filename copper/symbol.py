class Symbol:
    fn = None
    depends = None
    nocache = False
    def __init__(self, fn):
        if isinstance(fn, Symbol):
            self.fn = fn.fn
            self.depends = fn.depends
            self.nocach = fn.nocache
        else:
            self.fn = fn
            self.depends = []
            self.nocache = False
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
    @property
    def inputs(self):
        code = self.fn.__code__
        return code.co_varnames[:code.co_argcount]

class Task(Symbol):
    def __str__(self):
        return '<Task {}>'.format(self.name)

class Variable(Symbol):
    def __str__(self):
        return '<Variable {}>'.format(self.name)

