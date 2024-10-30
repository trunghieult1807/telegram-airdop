from utils.api_detector import ApiDetector

app_name = 'seed'
app_url = 'https://cf.seeddao.org/'
target_apis = {
    'https://elb.seeddao.org',
}
ignore_js_scripts = {
    'https://telegram.org/js/telegram-web-app.js',
    'https://tganalytics.xyz/index.js',
}
header = {
    'accept': '*/*',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}
headerjs = {
    'accept': '*/*',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}

detector = ApiDetector(app_name, app_url, target_apis, ignore_js_scripts, header, headerjs)
