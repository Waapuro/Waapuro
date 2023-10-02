import html

from lxml import etree

from waapuro import settings
from waapuro_code.tags_mapping import WaapuroCode


class WC2HTML(WaapuroCode):
    def parse(self, wc_content_str=None):
        """
        Parse content to HTML
        return: HTML string
        """
        keep_tags = settings.WAAPUROCODE_CONTENT_TAG

        if wc_content_str:
            _content_root = etree.fromstring(wc_content_str)
        else:
            _content_root = self.get_content()

        def clean_tags(element):
            for sub_element in element[:]:
                if sub_element.tag not in keep_tags:
                    element.remove(sub_element)
                else:
                    clean_tags(sub_element)

        clean_tags(_content_root)
        xml_string = etree.tostring(_content_root, pretty_print=True, encoding='utf-8').decode('utf-8')
        return html.unescape(xml_string)

    def parse_min(self):
        delete = ["  ", "\r", "\n"]
        content = self.parse()
        for d in delete:
            content = content.replace(d, "")
        return content
