level = 1

def debug_enter(*msg):
    global level
    print '{}> {}'.format('-'*level, msg)
    level += 1

def debug_exit(*msg):
    global level
    level -= 1
    print '{}< {}'.format('-'*level, msg)

class Symbol:
    @staticmethod
    def make(sym):
        return sym if isinstance(sym, Symbol) else Symbol(sym)

    def __init__(self, fn):
        self.ctx = None
        self.fn = fn
        self.parents = []
        self.children = []
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
    def varnames(self):
        code = self.fn.__code__
        return code.co_varnames[:code.co_argcount]

    @property
    def varitems(self):
        return [(v, self.ctx.variables[v]) for v in self.varnames]

    def register(self, ctx):
        for parent in self.parents:
            parent.children.append(self)
        self.ctx = ctx

    def __call__(self, *args, **kwds):
        vs = self.varnames()
        for i in range(min(len(args), len(vs))):
            kwds[vs[i]] = args[i]
        return self.resolve(**kwds)

    def depends(self, tasks):
        self.parents.extend(tasks)

    def filter(self, args):
        return { k:(v if not isinstance(v, list) or len(v) > 1 else v[0]) for k,v
                in args.iteritems() if k in self.varnames and v }

    def expand(self, args):
        debug_enter('expand', self.name, args)
        inputs = [{}]
        for key, sym in self.varitems:
            avail = sym.resolve(**args)
            values = args[key] if key in args else avail
            if not isinstance(values, list): values = [values]
            new_inputs = []
            for val in values:
                if not val in avail:
                    raise ValueError('{}: {}'.format(key, val))
                for inp in inputs:
                    new_inp = inp.copy()
                    new_inp[key] = val
                    new_inputs.append(new_inp)
            inputs = new_inputs
        debug_exit(inputs)
        return inputs

    def resolve(self, **args):
        debug_enter('resolve', self.name, args)
        args = self.filter(args)
        for parent in self.parents:
            parent.resolve_all(**args)
        ret = self.fn(**args)
        debug_exit(ret)
        return ret

    def resolve_all(self, **args):
        args = self.filter(args)
        inputs = self.expand(args)
        for inp in inputs:
            self.resolve(**inp)


