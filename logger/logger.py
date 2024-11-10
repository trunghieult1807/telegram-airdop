import sys
from loguru import logger
from utils.config import settings
from utils.tg_bot import notification_sink

logger.remove()
logformat = "<white>{time:YYYY-MM-DD HH:mm:ss}</white> | <level>{level: <8}</level> | {extra[tag]} | <cyan><b>{line}</b></cyan> - <white><b>{message}</b></white>"

if settings.USE_TELEGRAM_NOTI: 
    logger.add(notification_sink, level="ERROR")
    
logger.add(sink=sys.stdout, format=logformat, colorize=True)
logger = logger.opt(colors=True)

glogger = logger.bind(tag="SYSTEM")
