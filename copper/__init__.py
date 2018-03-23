from functools import wraps

def task(fn):
    @wraps(fn)
    def wrapper(*args, **kwds):
        return fn(*args, **kwds)
    return wrapper

def variable(fn):
    @wraps(fn)
    def wrapper(*args, **kwds):
        return fn(*args, **kwds)
    return wrapper

def depends(*ts):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwds):
            return fn(*args, **kwds)
        return wrapper
    return decorator

def main():
    print 'Hello, copper!'
