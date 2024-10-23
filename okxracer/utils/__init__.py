from .logger import logger

import os

if not os.path.exists(path="sessions"):
    os.mkdir(path="sessions")
