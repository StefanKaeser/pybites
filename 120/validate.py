from functools import wraps

def int_args(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        for arg in args:
            if type(arg) != int:
                raise TypeError
            if arg < 0:
                raise ValueError
        return func(*args, **kwargs)
    return decorate
