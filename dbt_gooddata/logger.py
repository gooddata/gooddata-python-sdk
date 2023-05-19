import logging
import sys


def get_logger(name, debug=False):
    level = logging.INFO if not debug else logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)-8s: %(name)s : %(asctime)-15s - %(message)s")
    logger = logging.getLogger(name)
    return logger
