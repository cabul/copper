from tinydb import Query, where
from .error import CopperError

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
        self.children = []
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
        return { k:v for k,v in args.iteritems() if k in self.varnames and v }

    def filter_all(self, args):
        return { k:(v if isinstance(v, list) else [v])
            for k,v in args.iteritems() if k in self.varnames and v }

    def expand(self, args):
        def expand_rec(varitems, inputs, args):
            if len(varitems) == 0: return inputs
            (key, var), rest = varitems[0], varitems[1:]
            new_inputs = []
            for inp in inputs:
                avail = var.resolve(inp)
                values = args[key] if key in args else avail
                for val in values:
                    if not val in avail:
                        raise CopperError('invalid {}: {}'.format(key, val))
                    new_inp = inp.copy()
                    new_inp[var.name] = val
                    new_inputs.append(new_inp)
            return expand_rec(rest, new_inputs, args)
        return expand_rec(self.varitems, [{}], args)

    def read_cache(self, args):
        qu = where('name') == self.name
        for k, v in args.iteritems():
            qu = qu & (where('var')[k] == v)
        row = self.ctx.db.get(qu)
        if not row: return False, None
        return True, row['ret']

    def write_cache(self, args, ret):
        self.invalidate(args)
        self.ctx.db.insert({
            'name': self.name,
            'var': args,
            'ret': ret
        })

    def invalidate(self, args):
        args = self.filter(args)
        qu = where('name') == self.name
        for k, v in args.iteritems():
            qu = qu & (where('var')[k] == v)
        rows = self.ctx.db.search(qu)
        self.ctx.db.remove(doc_ids=[row.doc_id for row in rows])

    def resolve(self, args, force=False):
        args = self.filter(args)
        for parent in self.parents:
            parent.resolve_all(args)
        found, old = self.read_cache(args)
        if found and not force: return old
        ret = self.fn(**args)
        if found and old == ret and old != None: return ret
        if not self.nocache:
            self.write_cache(args, ret)
        for child in self.children:
            child.invalidate(args)
        return ret

    def resolve_all(self, args, force=False):
        args = self.filter_all(args)
        inputs = self.expand(args)
        ret = []
        for inp in inputs:
            ret.append((inp, self.resolve(inp, force)))
        return ret


