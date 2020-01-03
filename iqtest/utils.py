import sys
import os
from functools import wraps
import traceback


def safe_one_retval_wrapper(f):
    """ add wrapper for function with one return value
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return None, f(*args, **kwargs)
        except Exception:
            return traceback.format_exc(), None

    return wrapper
