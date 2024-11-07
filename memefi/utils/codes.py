from aiohttp import ClientSession
from asyncio import sleep
from time import time
from json import loads, dump
from os import path

from memefi.utils.logger import logger



class Code:

    id: str
    name: str
    code: str
    link: str

    def __init__(self, data: dict):
        self.name = data['name']
        self.code = data.get('code', '')
        self.id = data.get("id")
        self.link = data.get('link')

    def dict(self, with_video_link = False) -> dict:
        data = {"name": self.name, "code": self.code}
        if self.id:
            data.update({"id": self.id})
        if with_video_link and self.link:
            data.update({"link": self.link})
        return data

CodesType = dict[str, Code]

class VideoCodes:

    codes_urls = [
        "https://raw.githubusercontent.com/ArthurKoba/MemeFiBot/main/codes.json",
        "https://raw.githubusercontent.com/sirbiprod/MemeFiBot/main/codes.json"
    ]

    filename = "codes.json"

    _codes_id: CodesType = {}
    _codes_name: CodesType = {}
    _incorrect_codes: CodesType = {}
    _existing_codes: CodesType = {}

    _last_update_timestamp: int = 0
    _last_update_from_external_codes_timestamp: float = 0
    _last_edit_timestamp_local_codes_file: float = 0
    _checkpoint_need_update_local_file = False

    @staticmethod
    def _get_codes_from_data(data: dict) -> CodesType:
        codes = {}
        for code in data:
            if not code["code"]:
                continue
            codes[code["name"]] = Code(code)
        return codes


    async def _load_codes_from_url(self, url: str) -> CodesType:
        try:
            async with ClientSession() as session:
                request = await session.get(url=url, timeout=5)
                if request.status == 200:
                    response = await request.text()
                    codes_data = loads(response).get("codes", [])
                    logger.info(f"Loaded {len(codes_data)} codes from {url}.")
                    return self._get_codes_from_data(codes_data)
                if request.status == 404:
                    logger.error(f"Failed to load codes from {url}.")
        except Exception as e:
            logger.error(f"Error when try get codes: {e}", url)
        return {}

    def get_codes_with_local_file(self, filename: str) -> CodesType:
        with open(filename, "r") as f:
            codes_data = loads(f.read()).get("codes", [])
            logger.info(f"Loaded {len(codes_data)} codes from local file.")
            return self._get_codes_from_data(codes_data)

    async def update_video_codes(self):
        codes_named = {}

        if time() - self._last_update_from_external_codes_timestamp > 60 * 5:
            self._last_update_from_external_codes_timestamp = time()
            for url in self.codes_urls:
                codes_named.update((await self._load_codes_from_url(url)))

        if self._last_edit_timestamp_local_codes_file != path.getmtime(self.filename):
            self._last_edit_timestamp_local_codes_file = path.getmtime(self.filename)
            codes_named.update(self.get_codes_with_local_file(self.filename))

        count_updates = 0
        self._codes_id = {}
        for name in codes_named.keys():
            code_obj = codes_named[name]
            if code_obj.id and code_obj.id not in self._codes_id:
                self._codes_id.update({code_obj.id: code_obj})
            if name in self._codes_name and code_obj.code == self._codes_name[name].code:
                continue
            if name in self._incorrect_codes and code_obj.code != self._incorrect_codes[name].code:
                self._incorrect_codes.pop(name)
            count_updates += 1
            self._codes_name[name] = code_obj
        if count_updates:
            logger.debug(f"VideoCodes | Successful loaded {count_updates} video codes.")
            self._last_update_timestamp = int(time())

    async def run_updater(self):
        while True:
            await self.update_video_codes()
            if self._checkpoint_need_update_local_file and time() - self._checkpoint_need_update_local_file > 10:
                self.update_local_file()
            await sleep(1)


    def update_local_file(self):
        self._checkpoint_need_update_local_file = None
        with open(self.filename, mode="w") as f:
            dump({
                "incorrect_codes": [code.dict(with_video_link=True) for code in self._incorrect_codes.values()],
                "existing_codes": [code.dict(with_video_link=True) for code in self._existing_codes.values()],
                "codes": [code.dict() for code in self._codes_name.values() if code.code]
            }, f, indent=2, ensure_ascii=False)
        self._last_edit_timestamp_local_codes_file = path.getmtime(self.filename)

    def mark_code_as_incorrect(self, task: dict):
        video = Code(task)
        video.code = self._codes_name.pop(video.name).code
        logger.warning(f"VideoCodes | Mark code {video.code} as incorrect from video {video.name}")
        self._incorrect_codes[video.name] = video
        if video.id and video.id in self._codes_id:
            self._codes_id.pop(video.id)
        self._checkpoint_need_update_local_file = time()

    def mark_code_as_correct(self, task: dict, code):
        video = Code(task)
        video.code = code
        if video.name in self._incorrect_codes:
            self._incorrect_codes.pop(video.name)
        elif video.id in self._existing_codes:
            self._existing_codes.pop(video.id)
        else:
            return
        self._checkpoint_need_update_local_file = time()


    def get_video_code(self, task: dict) -> str | None:
        video = Code(task)
        try:
            if video.name in self._incorrect_codes:
                video.code = self._incorrect_codes[video.name].code
                self._incorrect_codes[video.name] = video
                return None
            if video.id in self._codes_id and self._codes_id[video.id].code:
                return self._codes_id[video.id].code
            if video.name in self._codes_name and self._codes_name[video.name].code:
                return self._codes_name[video.name].code
            self._existing_codes.update({video.id: Code(task)})
            self._checkpoint_need_update_local_file = time()
        except Exception as e:
            logger.error(f"VideoCodesError: {e.__name__}: {e}")



    def get_last_update_timestamp(self) -> int:
        return self._last_update_timestamp