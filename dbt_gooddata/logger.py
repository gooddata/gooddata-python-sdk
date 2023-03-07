import logging
import sys


def get_logger(name, debug=False):
    level = logging.INFO if not debug else logging.DEBUG
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        channel = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(fmt='%(levelname)-8s: %(name)s : %(asctime)-15s - %(message)s')
        channel.setFormatter(formatter)
        logger.addHandler(channel)
    return logger
