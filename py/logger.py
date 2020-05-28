import logging
from functools import wraps
import time

now = lambda: time.time()


def logger(log_file=''):
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger


def log(out_put, log_file='', level=''):
    def deco(f):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if log_file:
            handler = logging.FileHandler(log_file)
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        _level_dict = {'info': logger.info,
                      'debug': logger.debug,
                      'error': logger.error,
                      'warn': logger.warn}

        @wraps(f)
        def wrapper(*args, **kwargs):
            _level_dict.get(level, logger.info)(out_put)
            f(*args, **kwargs)
        return wrapper
    return deco


@log('haha')
def test2():
    pass


def profile(f):
    def wrapper(*args, **kwargs):
        start = now()
        f(*args, **kwargs)
        end = now()
        print('total cost: %.2f' %(end - start))
    return wrapper


@profile
def test1():
    time.sleep(1.2)


if __name__ == '__main__':
    test1()
    test2()

