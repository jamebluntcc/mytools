"""
使用 logging 作为 logger 输出
"""
import os
import logging

def setup_custom_logger(name, log_level, console=True):
    fmt = "%(asctime)-15s %(levelname)s %(module)s %(message)s"
    formatter = logging.Formatter(fmt)
    if console:
        handler = logging.StreamHandler()
    else:
        log_path = os.path.join(os.getcwd(), 'test.log')
        handler = logging.FileHandler(log_path)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger

if __name__ == '__main__':
    name = "root"
    log_level = logging.INFO
    logger = setup_custom_logger(name, log_level, console=False)
    logger.info('haha')
