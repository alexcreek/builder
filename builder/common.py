import logging

def setup_logger(name, path=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if path:
        handler = logging.FileHandler(filename=path, mode='a')
        fmt = '%(asctime)s %(message)s'
    else:
        handler = logging.StreamHandler()
        fmt = '%(asctime)s %(levelname)s %(message)s'

    formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
