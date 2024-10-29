from utils.api_detector import ApiDetector

def main():
    ignore_js_scripts = {
        'https://telegram.org/js/telegram-web-app.js',
        'https://tganalytics.xyz/index.js',
        './pixi.min.js',
        './viewport.min.js',
    }
    apis = {
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
    base_url = "https://app.notpx.app/"
    detector = ApiDetector('notpixel', base_url, apis, ignore_js_scripts)
    print(detector.check_api())

if __name__ == '__main__':
    main()
