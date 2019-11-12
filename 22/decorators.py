from functools import wraps


def make_html(element):
    left_braket = "<%s>"%element
    right_braket = "</%s>"%element

    def decorate(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            text = func(*args, **kwargs)
            text = left_braket + text + right_braket
            return text

        return wrapped

    return decorate

