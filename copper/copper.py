from symbol import Symbol, Task, Variable
from collections import OrderedDict
from argparse import ArgumentParser
from tinydb import TinyDB, Query

def depends(*ts):
    def decorator(fn):
        sym = Symbol(fn)
        sym.depends.extend(ts)
        return sym
    return decorator

def nocache(sym):
    sym = Symbol(sym)
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
        sym = Variable(sym)
        self.variables[sym.name] = sym
        return sym
    def task(self, sym):
        sym = Task(sym)
        self.tasks[sym.name] = sym
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
        parser.add_argument('task', nargs='?', help='see -l for a list of tasks')
        args = parser.parse_args()
        if args.clean:
            self.clean()
            return
        if not args.task or args.list:
            self.list()
            return

