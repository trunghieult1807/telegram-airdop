import sys
from scripts.utils import empty_directory
from logger.logger import glogger
from utils.api_detector import save_api_data, DATA_DIR
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

def init_antiban():
    for detector in detectors:
        detector.init_api_data()
        glogger.success(f"{detector.app_name} api data initialized")
    mark_safe_apis()

def mark_safe_apis():
    for detector in detectors:
        if detector.mark_safe():
            glogger.success(f"{detector.app_name} is safe")
        else:
            glogger.error(f"{detector.app_name} is NOT safe")

def check_apis():
    for detector in detectors:
        if detector.check_api():
            glogger.success(f"{detector.app_name} is safe")
        else:
            glogger.error(f"{detector.app_name} is NOT safe")


def run():
    match sys.argv[1]:
        case 'init':
            init_antiban()
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
