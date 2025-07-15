import logging
from logging.handlers import RotatingFileHandler
from src.config.settings import LOG_DIR


def get_logger(name):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    fh = RotatingFileHandler(
        LOG_DIR / "transporte.log",
        maxBytes=3 * 1024 * 1024,
        backupCount=2,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger
