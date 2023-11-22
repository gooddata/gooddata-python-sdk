# (C) 2023 GoodData Corporation
import logging


def get_logger(name: str, debug: bool = False) -> logging.Logger:
    level = logging.INFO if not debug else logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)-8s: %(name)s : %(asctime)-15s - %(message)s")
    logger = logging.getLogger(name)
    return logger
