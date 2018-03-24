from symbol import Symbol
from collections import OrderedDict
from argparse import ArgumentParser
from tinydb import TinyDB, Query
import sys

def depends(*ts):
    def decorator(fn):
        sym = Symbol.make(fn)
        sym.depends(ts)
        return sym
    return decorator

def nocache(sym):
    sym = Symbol.make(sym)
    sym.nocache = True
    return sym

class Copper:
    description = None
    variables = None
    tasks = None
    db = None

    def __init__(self, description='', cache='.copper.json'):
        self.description = description
        self.variables = OrderedDict()
        self.tasks = OrderedDict()
        self.db = TinyDB(cache)

    def variable(self, sym):
        sym = Symbol.make(sym)
        self.variables[sym.name] = sym
        sym.register(self)
        return sym
    def task(self, sym):
        sym = Symbol.make(sym)
        self.tasks[sym.name] = sym
        sym.register(self)
        return sym

    def clean(self):
        self.db.purge()

    def list_dict(self, d):
        max_len = max([len(k) for k in d.keys()])
        for k, v in d.iteritems():
            if v.doc:
                pad = ' ' * (max_len - len(k))
                print '  {}{} - {}'.format(k, pad, v.doc)
            else:
                print '  {}'.format(k)

    def list(self):
        print 'Variables:'
        self.list_dict(self.variables)
        print 'Tasks:'
        self.list_dict(self.tasks)

    def main(self):
        parser = ArgumentParser(prog='copper', description=self.description)
        parser.add_argument('-c', '--clean', action='store_true', help='clean copper cache')
        parser.add_argument('-l', '--list', action='store_true', help='list copper tasks/variables')
        parser.add_argument('-f', '--force', action='store_true', help='force cache overwrite')
        parser.add_argument('task', nargs='?', help='see -l for a list of tasks')
        for name, var in self.variables.iteritems():
            parser.add_argument('--{}'.format(name), nargs='+', help=var.doc)
        args = parser.parse_args()
        if args.clean:
            self.clean()
            return
        if not args.task or args.list:
            self.list()
            return
        try:
            task = self.tasks[args.task]
            task.resolve_all(vars(args), args.force)
        except KeyError as e:
            print >> sys.stderr, 'copper: error: unrecognized task: {}'.format(e)
            sys.exit(1)
        except ValueError as e:
            print >> sys.stderr, 'copper: error: invalid value for {}'.format(e)
            sys.exit(1)

