import re
import uuid
import pykakasi

from lxml import etree

from waapuro_code.tags_mapping import WaapuroCode


class Aozora2WC(WaapuroCode):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.aozora_profile = None
        self.aozora_lines = None
        self.aozora_text = kwargs.get("aozora_text")

    @staticmethod
    def _romaji(kanji):
        kks = pykakasi.kakasi()
        result = kks.convert(kanji)
        return result[0]['passport']

    def get_aozora_lines(self):
        self.aozora_lines = self.aozora_text.split("\n")
        return self.aozora_lines

    def get_aozora_profile(self, url=None):
        self.get_aozora_lines()
        # The 1st line -> TITLE
        title = self.aozora_lines[0]
        # The 2nd line -> Real Author
        real_author = self.aozora_lines[0]

        self.aozora_profile = {
            "url": url if url else self._romaji(title),
            "title": title,
            "type": "post",
            "tags": ["Auto-Aozora2WC", real_author, title],
            "status": "published",
            "last_version": None,
            "id": uuid.uuid4(),
            "category": "青空文庫",
            "excerpt": "",
            "publish_time": "",
            "author": None,
        }
        return self.aozora_profile
