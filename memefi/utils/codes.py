from aiohttp import ClientSession
from asyncio import sleep
from random import randint
from json import loads
from memefi.utils.logger import logger


CodesType = dict[str, str]

class VideoCodes:

    _codes: CodesType = {}

    @staticmethod
    async def _load_codes_from_url(url: str) -> CodesType:
        try:
            async with ClientSession() as session:
                request = await session.get(url=url, timeout=5)
                if request.status == 200:
                    response = await request.text()
                    codes_data = loads(response).get("codes", [])
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

    async def update_video_codes(self):
        with open("codes.json", "r") as f:
            codes_data = loads(f.read()).get("codes", [])
            for code in codes_data:
                self._codes[code["name"]] = code["code"]

        codes_urls = [
            "https://raw.githubusercontent.com/ArthurKoba/MemeFiBot/main/codes.json",
            "https://raw.githubusercontent.com/sirbiprod/MemeFiBot/main/codes.json"
        ]

        for url in codes_urls:
            self._codes.update((await self._load_codes_from_url(url)))
        logger.info(f"VideoCodes | Successful loaded {len(self._codes.keys())} video codes.")

    async def run_updater(self):
        while True:
            await self.update_video_codes()
            await sleep(60*30)

    def get_video_codes(self) -> CodesType:
        return self._codes

    def get_video_code(self, video_name: str) -> str | None:
        return self._codes.get(video_name)
