from collections import OrderedDict
from tinydb import TinyDB, Query

db = TinyDB('.copper.json')
tasks = OrderedDict()
variables = OrderedDict()

def list_dict(d):
    max_len = max([len(k) for k in d.keys()])
    for k, v in d.iteritems():
        if v.doc:
            padding = ' ' * (max_len - len(k))
            print'  {}{} - {}'.format(k, padding, v.doc)
        else:
            print '  {}'.format(k)

def list_items():
    print 'Variables:'
    list_dict(variables)
    print 'Tasks:'
    list_dict(tasks)
