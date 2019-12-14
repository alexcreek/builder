import logging

def init_logging(name, path=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if path:
        handler = logging.FileHandler(filename=path, mode='a')
    else:
        handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


