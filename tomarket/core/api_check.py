import requests
import re
from tomarket.utils import logger

baseUrl = "https://api-web.tomarket.ai/tomarket-game/v1"

def get_main_js_format(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        content = response.text
        
        matches = re.findall(r'src="(/.*?/index.*?\.js)"', content)
        if matches:
            return sorted(set(matches), key=len, reverse=True)
        else:
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching the base URL: {e}")
        return None

def get_base_api(url):
    try:
        logger.info(f"Fetching JS file from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        search_string = 'online:"https://api-web.tomarket.ai/tomarket-game/v1"'

        if search_string in content:
            return True
        else:
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching the JS file: {e}")
        return None

def check_base_url():
    base_url = "https://mini-app.tomarket.ai/"
    main_js_formats = get_main_js_format(base_url)

    if main_js_formats:
        for format in main_js_formats:
            full_url = f"https://mini-app.tomarket.ai{format}"
            logger.info(f"Trying format: {full_url}")
            result = get_base_api(full_url)

            if result:
                logger.info("<green>No change in API!</green>")
                return True
            else:
                logger.warning(f"API might have changed, bot stopped for safety.")
                return False
    else:
        logger.info("Could not find any main.js format. Dumping page content for inspection:")
        try:
            response = requests.get(base_url)
            logger.info(response.text[:1000])
        except requests.RequestException as e:
            logger.info(f"Error fetching the base URL for content dump: {e}")
        return False