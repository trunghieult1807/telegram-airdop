from logger.logger import logger

logger = logger.bind(tag="Blum")

def info(text):
    return logger.info(text)


def debug(text):
    return logger.debug(text)


def warning(text):
    return logger.warning(text)


def error(text):
    return logger.error(text)


def critical(text):
    return logger.critical(text)


def success(text):
    return logger.success(text)