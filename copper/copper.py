from symbol import make_symbol

def depends(*ts):
    def decorator(sym):
        sym = make_symbol(sym)
        return sym
    return decorator

def nocache(sym):
    sym = make_symbol(sym)
    return sym

class Copper:
    description = None

    def __init__(self, description=''):
        self.description = description

    def variable(self, sym):
        sym = make_symbol(sym)
        return sym
    def task(self, sym):
        sym = make_symbol(sym)
        return sym

    def main(self):
        print 'Hello, copper!'

