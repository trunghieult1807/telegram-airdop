from .logger import logger, info, warning, debug, success, error, critical

import os

if not os.path.exists(path="sessions"):
    os.mkdir(path="sessions")
