import sys
from loguru import logger
import requests
import time
from collections import defaultdict
from utils.config import settings

# Dictionary to store timestamps of requests for each appName
request_log = defaultdict(list)

def is_rate_limited(app_name, limit=3, window=60):
    """Check if appName has exceeded rate limit within the time window (in seconds)."""
    current_time = time.time()
    
    recent_requests = [timestamp for timestamp in request_log[app_name] if current_time - timestamp < window]
    request_log[app_name] = recent_requests
    
    if len(recent_requests) >= limit:
        return True
    
    request_log[app_name].append(current_time)
    return False

def api_error_sink(message):
    bot_token = settings.BOT_TOKEN
    chat_id = settings.CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
   
    try:
        record = message.record
        log_message = record["message"]
        appName = record["extra"].get("tag", "")  
        line = record["line"]
        
        # Check rate limit
        if is_rate_limited(appName):
            logger.bind(tag="SYSTEM").warning(f"Rate limit exceeded for {appName}, skipping notification.")
            return
        
        # Format the final notification message
        notification_message = (
            f"<b>{appName}</b> | "  # Bold the app name
            f"<code>{line}</code> - "  # Show the line in code format
            f"<i>{log_message}</i>"  # Italicize the log message
        )
        
        payload = {
            'chat_id': chat_id,
            'text': notification_message,
            'parse_mode': 'HTML'  # Optional: allows HTML formatting in the message
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.bind(tag="SYSTEM").info(f"Notification sent: {response.status_code}")
    except requests.RequestException as e:
        logger.bind(tag="SYSTEM").error(f"Send notification failed: {e}")

logger.remove()
logformat = "<white>{time:YYYY-MM-DD HH:mm:ss}</white> | <level>{level: <8}</level> | {extra[tag]} | <cyan><b>{line}</b></cyan> - <white><b>{message}</b></white>"

if settings.USE_TELEGRAM_NOTI: 
    logger.add(api_error_sink, level="ERROR")
    
logger.add(sink=sys.stdout, format=logformat, colorize=True)
logger = logger.opt(colors=True)
