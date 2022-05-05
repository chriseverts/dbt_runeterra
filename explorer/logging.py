import logging

default_handler = logging.StreamHandler()
default_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
)


def get_logger(name):
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(default_handler)

    return logger
