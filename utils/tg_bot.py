import requests
import time
import sys
from collections import defaultdict
from .config import settings
from loguru import logger

def is_rate_limited(app_name, limit=settings.CHAT_LIMIT, window=settings.CHAT_LIMIT_WINDOW):
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
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
   
    try:
        record = message.record
        log_message = record["message"]
        appName = record["extra"].get("tag", "")  
        line = record["line"]
        level = record["level"].name 

        if level == "ERROR":
            chat_id = settings.ERROR_CHAT_ID
        elif level == "CRITICAL":
            chat_id = settings.CRITICAL_CHAT_ID
        else:
            return  
            
        # Check rate limit
        if is_rate_limited(appName):
            print(f"Rate limit exceeded for {appName}, skipping notification.", file=sys.stderr)
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
        print(f"Notification sent: {response.status_code}", file=sys.stderr)
    except requests.RequestException as e:
        print(f"Send notification failed: {e}", file=sys.stderr)
