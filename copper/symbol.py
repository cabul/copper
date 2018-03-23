from .backend import db, tasks, variables

class Symbol:
    fn = None
    def __init__(self, fn):
        self.fn = fn
        self.__name__ = fn.__name__
        self.__doc__ = fn.__doc__
    def __call__(*args, **kwds):
        return self.fn(*args, **kwds)
    
    @property
    def name(self):
        return self.fn.__name__
    @property
    def doc(self):
        return self.fn.__doc__
    @property
    def inputs(self):
        code = self.fn.__code__
        return code.co_varnames[:code.co_argcount]

class Task(Symbol):
    def __str__(self):
        return '<Task {}>'.format(self.name)
    def run(self, args):
        print self, args

class Variable(Symbol):
    def __str__(self):
        return '<Variable {}>'.format(self.name)
