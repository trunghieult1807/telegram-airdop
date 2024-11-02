from utils.api_detector import ApiDetector

app_name = 'coinsweeper'
app_url = 'https://bybitcoinsweeper.com/'
target_apis = {
    'https://api.bybitcoinsweeper.com/api',
    'auth/login',
    'auth/refresh-token',
    'games/lose',
    'games/start',
    'games/win',
}
ignore_js_scripts = {}

detector = ApiDetector(app_name, app_url, target_apis, ignore_js_scripts)
