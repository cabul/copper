class Copper:
    description = None

    def __init__(self, description=''):
        self.description = description

    def variable(self, fn):
        return fn
    def task(self, fn):
        return fn

    def main(self):
        print 'Hello, copper!'

def depends(*ts):
    def decorator(fn):
        return fn
    return decorator

def nocache(fn):
    return fn

