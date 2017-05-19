import time
from functools import wraps


def log_exec_time(func):
    """ Simple debug utility wrapper to log the execution time of the decorated function """
    @wraps(func)
    def __wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            return func(*args, **kwargs)
        finally:
            end_time = time.time()
            print('exec time >> {}ms'.format(end_time - start_time))

    return __wrapper

