from utils.api_detector import ApiDetector

app_name = 'notpixel'
app_url = 'https://app.notpx.app/'
target_apis = {
    '/users/me',
    '/mining/status',
    '/repaint/start',
    '/mining/boost/check/',
    '/mining/claim',
    '/image/template/my',
    '/image/template/',
    '/image/template/subscribe/',
    '/repaint/start',
    '/mining/task/check/',
}
ignore_js_scripts = {
    'https://telegram.org/js/telegram-web-app.js',
    'https://tganalytics.xyz/index.js',
    './pixi.min.js',
    './viewport.min.js',
}

detector = ApiDetector(app_name, app_url, target_apis, ignore_js_scripts)
