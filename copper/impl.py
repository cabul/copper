from functools import wraps
from argparse import ArgumentParser

import os

from .symbol import Variable, Task
from .backend import tasks, variables, db, list_items

def task(fn):
    t = Task(fn)
    tasks[t.name] = t
    return t

def variable(fn):
    v = Variable(fn)
    variables[v.name] = v
    return v

def depends(*ts):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwds):
            for t in ts: t(*args, **kwds)
            return fn(*args, **kwds)
        return wrapper
    return decorator

def main(description):
    
    parser = ArgumentParser(prog='copper', description=description)
    parser.add_argument('-c', '--clean', action='store_true', help='Clean copper cache')
    parser.add_argument('-l', '--list', action='store_true', help='List copper commands')
    parser.add_argument('-f', '--force', action='store_true', help='Force command execution')
    for k, v in variables.iteritems():
        parser.add_argument('--{}'.format(k), nargs='+', help=v.__doc__)
    parser.add_argument('task', nargs='?', help='see -l for a full list of tasks')
    args = parser.parse_args()
    if args.clean:
        db.purge()
    if not args.task or args.list:
        list_items()
    if not args.task: return
    task = tasks[args.task]
    task.run(vars(args))

