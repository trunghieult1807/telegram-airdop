import requests
import time
from collections import defaultdict
from .config import settings
from loguru import logger

def is_rate_limited(app_name, limit=settings.CHAT_LIMIT, window=settings.CHAT_LIMIT_WINDOW):
    """Check if appName has exceeded rate limit within the time window (in seconds)."""
    request_log = defaultdict(list)
    current_time = time.time()
    
    recent_requests = [timestamp for timestamp in request_log[app_name] if current_time - timestamp < window]
    request_log[app_name] = recent_requests
    
    if len(recent_requests) >= limit:
        return True
    
    request_log[app_name].append(current_time)
    return False

def notification_sink(message):
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
