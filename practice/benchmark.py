import time as t
from functools import wraps


def print_duration(function, *args):
    start = t.time()
    function(*args)
    end = t.time()
    print("Function [", function.__name__, "] took", "%.4f" % (end - start), "milliseconds")


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = t.time()
        result = func(*args, **kwargs)
        stop = t.time()
        print(f"Function [{func.__name__}] took {stop - start:.4f} seconds")
        return result

    return wrapper


if __name__ == "__main__":

    @measure_time
    def test_time(timeout):
        t.sleep(timeout)

    test_time(5)
