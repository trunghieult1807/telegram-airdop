from aiohttp import ClientSession
from asyncio import sleep
from time import time
from json import loads
from memefi.utils.logger import logger


CodesType = dict[str, str]

class VideoCodes:

    codes_urls = [
        "https://raw.githubusercontent.com/ArthurKoba/MemeFiBot/main/codes.json",
        "https://raw.githubusercontent.com/sirbiprod/MemeFiBot/main/codes.json"
    ]

    _codes: CodesType = {}
    _incorrect_codes: CodesType = {}
    _last_update_timestamp: int = 0
    _last_update_from_external_codes_timestamp: float = 0
    _last_edit_timestamp_local_codes_file: float = 0

    @staticmethod
    async def _load_codes_from_url(url: str) -> CodesType:
        try:
            async with ClientSession() as session:
                request = await session.get(url=url, timeout=5)
                if request.status == 200:
                    response = await request.text()
                    codes_data = loads(response).get("codes", [])
                    logger.info(f"Loaded {len(codes_data)} codes from {url}.")
                    codes = {}
                    for code in codes_data:
                        if not code["code"]:
                            continue
                        codes[code["name"]] = code["code"]
                    return codes
                if request.status == 404:
                    logger.error(f"Failed to load codes from {url}.")
        except Exception as e:
            logger.error(f"Error when try get codes: {e}", url)
        return {}

    @staticmethod
    def get_codes_with_local_file(filename: str) -> CodesType:
        codes = {}
        with open(filename, "r") as f:
            codes_data = loads(f.read()).get("codes", [])
            logger.info(f"Loaded {len(codes_data)} codes from local file.")
            for code in codes_data:
                if not code["code"]:
                    continue
                codes[code["name"]] = code["code"]
        return codes


    async def update_video_codes(self):
        codes = {}
        if self._last_edit_timestamp_local_codes_file != path.getmtime("codes.json"):
            self._last_edit_timestamp_local_codes_file = path.getmtime("codes.json")
            codes.update(self.get_codes_with_local_file("codes.json"))

        if time() - self._last_update_from_external_codes_timestamp > 60 * 5:
            self._last_update_from_external_codes_timestamp = time()
            for url in self.codes_urls:
                codes.update((await self._load_codes_from_url(url)))

        count_updates = 0
        for video_name in codes.keys():
            if video_name in self._codes and codes[video_name] == self._codes[video_name]:
                continue
            if video_name in self._incorrect_codes and codes[video_name] != self._incorrect_codes[video_name]:
                self._incorrect_codes.pop(video_name)
            count_updates += 1
            self._codes[video_name] = codes[video_name]
        if count_updates:
            logger.info(f"VideoCodes | Successful loaded {count_updates} video codes.")
            self._last_update_timestamp = int(time())

    async def run_updater(self):
        while True:
            await self.update_video_codes()
            await sleep(1)

    def mark_code_as_incorrect(self, name: str, code: str):
        logger.warning(f"VideoCodes | Mark code {code} as incorrect from video {name}")
        self._incorrect_codes[name] = code

    def get_video_codes(self) -> CodesType:
        return self._codes

    def get_video_code(self, video_name: str) -> str | None:
        if video_name in self._incorrect_codes:
            return None
        return self._codes.get(video_name)

    def get_last_update_timestamp(self) -> int:
        return self._last_update_timestamp