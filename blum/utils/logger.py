import sys
from blum.config import settings
from typing import Callable

from logger.logger import logger

logger = logger.bind(tag="Blum")

MessageMethod = Callable[[str], None]

def disable_color_on_error(formatter, level_):
    def wrapper(*args, **kwargs):
        try:
            getattr(logger, level_)(formatter(*args, **kwargs))
        except ValueError:
            getattr(logger.opt(colors=False), level)(*args, **kwargs)
    return wrapper

class SessionLogger:

    session_name: str
    trace: MessageMethod
    debug: MessageMethod
    info: MessageMethod
    success: MessageMethod
    warning: MessageMethod
    error: MessageMethod
    critical: MessageMethod

    def __init__(self, session_name):
        self.session_name = session_name
        for method_name in ("trace", "debug", "info", "success", "warning", "error", "critical"):
            setattr(self, method_name, disable_color_on_error(self._format, method_name))

    def _format(self, message):
        return f"{self.session_name} | {message}"