from utils.api_detector import ApiDetector

app_name = 'tomarket'
app_url = 'https://mini-app.tomarket.ai/'
target_apis = {
    'https://api-web.tomarket.ai/tomarket-game/v1',
}
ignore_js_scripts = {}

detector = ApiDetector(app_name, app_url, target_apis, ignore_js_scripts)
