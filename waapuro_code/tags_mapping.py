import xmltodict as xmltodict
from lxml import etree
import xmltodict

from waapuro import settings


class WC2HTML:
    """
    WaapuroCode To Html
    """

    def __init__(self, wc="<waapuro></waapuro>"):
        self._wc = str(wc)
        self._load()

    def parse(self):
        """
        Parse content to HTML
        return: HTML string
        """
        keep_tags = settings.WAAPUROCODE_CONTENT_TAG
        _content_root = self.get_content()

        def clean_tags(element):
            for sub_element in element[:]:
                if sub_element.tag not in keep_tags:
                    element.remove(sub_element)
                else:
                    clean_tags(sub_element)

        clean_tags(_content_root)

        return etree.tostring(_content_root, pretty_print=True, encoding='utf-8').decode('utf-8')

    def parse_min(self):
        delete = ["  ", "\r", "\n"]
        content = self.parse()
        for d in delete:
            content = content.replace(d, "")
        return content

    def _load(self):
        self.waapuro_root = etree.fromstring(self._wc)

    def set_waapurocode(self, wc):
        self._wc = str(wc)
        self._load()

    def get_profile(self):
        """
        Get profile (dict)
        """
        profile_str = etree.tostring(self.waapuro_root.find("profile"))
        return xmltodict.parse(profile_str)["profile"]

    def get_content(self):
        """
        Get profile (lxml)
        """
        return self.waapuro_root.find("content")


if __name__ == '__main__':
    w2h = WC2HTML()
    with open('../configs_demo/demo.waapuro', 'r', encoding='utf-8') as file:
        w2h.set_waapurocode(file.read())

    print(w2h.get_profile())
    print(w2h.parse_min())
