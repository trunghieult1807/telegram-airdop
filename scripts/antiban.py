import sys
from logger.logger import glogger
from coinsweeper.utils.detector import detector as coinsweeper_detector
from notpixel.utils.detector import detector as notpixel_detector
from seed.utils.detector import detector as seed_detector
from tomarket.utils.detector import detector as tomarket_detector

detectors = [
    coinsweeper_detector,
    notpixel_detector,
    seed_detector,
    tomarket_detector,
]

def init():
    for detector in detectors:
        detector.init_api_data()
        glogger.success(f"{detector.app_name} api data initialized")

def mark_safe_apis():
    for detector in detectors:
        if detector.mark_safe():
            glogger.success(f"{detector.app_name} marked as SAFE")
        else:
            glogger.error(f"{detector.app_name} marked as UNSAFE")

def check_apis():
    for detector in detectors:
        if detector.check_api():
            glogger.success(f"{detector.app_name} is safe")
        else:
            glogger.error(f"{detector.app_name} is NOT safe")


def run():
    match sys.argv[1]:
        case 'setup':
            init()
            mark_safe_apis()
        case 'check':
            check_apis()
        case 'safe':
            mark_safe_apis()
        case _:
            raise Exception('Invalid command')

def main():
    try:
        run()
    except Exception as e:
        glogger.error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
