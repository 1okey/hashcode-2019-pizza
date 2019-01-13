import time as t


def print_duration(function, *args):
    start = t.time()
    function(*args)
    end = t.time()
    print('Function', function.__name__, 'took', '%.4f' % (end - start), 'milliseconds')
