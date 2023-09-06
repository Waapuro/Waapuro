"""
WaapuroCode > any
any > WaapuroCode
"""
import html
import re

from django.contrib.auth.models import User
from lxml import etree
import xmltodict

from waapuro import settings
from waapuro.publish.models import Status, PublishType, Article


def generate_field_mapping(profile):
    """
    This function generates a field mapping dictionary from a given profile.
    We apply special handling for the fields that are ForeignKey to assign the corresponding instances.


    # profile:
    wc = WaapuroCode()
    with open(p, 'r', encoding=settings.CHARSET) as file:
        wc.set_waapurocode(file.read())

    profile = wc.get_profile()
    """

    field_mapping = {
        'wc_id': profile.get('id', None),
        'url': profile.get('url', None),
        'last_version': profile.get('last_version', None),
        'title': profile.get('title', None),
        'excerpt': profile.get('excerpt', None),
        'publish_date': profile.get('publish_date', None),
        'content': profile.get('content', None),
    }

    # 特別な処理: status
    status_name = profile.get('status', None)
    if status_name:
        try:
            status_instance = Status.objects.get(name=status_name)
            field_mapping['status'] = status_instance
        except Status.DoesNotExist:
            field_mapping['status'] = None

    # 特別な処理: parent
    parent_id = profile.get('parent', None)
    if parent_id:
        try:
            parent_instance = Article.objects.get(wc_id=parent_id)
            field_mapping['parent'] = parent_instance
        except Article.DoesNotExist:
            field_mapping['parent'] = None

    # 特別な処理: author
    author_id = profile.get('author', None)
    if author_id:
        try:
            author_instance = User.objects.get(username=author_id)
            field_mapping['author'] = author_instance
        except User.DoesNotExist:
            field_mapping['author'] = None

    # 特別な処理: type
    type_name = profile.get('type', None)
    if type_name:
        try:
            type_instance = PublishType.objects.get(name=type_name)
            field_mapping['type'] = type_instance
        except PublishType.DoesNotExist:
            field_mapping['type'] = None

    return field_mapping


class WaapuroCode:
    """
    WaapuroCode To Html
    """

    def __init__(self, wc_str="<waapuro></waapuro>"):
        self._wc = wc_str
        self.set_waapurocode(wc_str)

    def _load(self):
        self.waapuro_root = etree.fromstring(self._wc)

    @staticmethod
    def _preprocess_xml(xml_str):
        # Function to preprocess XML string
        return re.sub(r'&(?!(?:amp|lt|gt|quot|apos);)', '&amp;', str(xml_str))

    def set_waapurocode(self, wc):
        self._wc = self._preprocess_xml(wc)
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


class WC2HTML(WaapuroCode):
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
        xml_string = etree.tostring(_content_root, pretty_print=True, encoding='utf-8').decode('utf-8')
        return html.unescape(xml_string)

    def parse_min(self):
        delete = ["  ", "\r", "\n"]
        content = self.parse()
        for d in delete:
            content = content.replace(d, "")
        return content


if __name__ == '__main__':
    wc = WaapuroCode()
    with open('../configs_demo/demo.waapuro', 'r', encoding='utf-8') as file:
        wc.set_waapurocode(file.read())

    print(wc.get_profile())

    w2h = WC2HTML()
    with open('../configs_demo/demo.waapuro', 'r', encoding='utf-8') as file:
        w2h.set_waapurocode(file.read())

    print(w2h.get_profile())
    print(w2h.parse_min())
