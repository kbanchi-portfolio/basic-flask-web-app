import logging
import logging.handlers
import os

from dotenv import load_dotenv

load_dotenv(verbose=True)


def get_logger():
    logger = logging.getLogger(__name__)
    # set logging level
    if os.environ.get("LOGGING_DEBUG"):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    # set logging file name
    rh = logging.handlers.RotatingFileHandler(
        r"./log/app.log", encoding="utf-8", maxBytes=1000, backupCount=3
    )
    # set logging format
    rh.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
    # add logging handler
    logger.addHandler(rh)
    return logger
