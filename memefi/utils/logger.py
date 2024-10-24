from logger.logger import logger

logger = logger.bind(tag="MemeFi")



class SessionLogger:

    session_name: str

    def __init__(self, session_name):
        self.session_name = session_name

    def debug(self, message):
        logger.debug(f"{self.session_name} | {message}")

    def info(self, message):
        logger.info(f"{self.session_name} | {message}")

    def success(self, message):
        logger.success(f"{self.session_name} | {message}")

    def warning(self, message):
        logger.warning(f"{self.session_name} | {message}")

    def error(self, message):
        logger.error(f"{self.session_name} | {message}")

    def critical(self, message):
        logger.critical(f"{self.session_name} | {message}")