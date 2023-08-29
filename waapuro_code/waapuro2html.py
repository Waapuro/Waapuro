import re


class Waapuro2HTML:
    def __init__(self, waapuro_code):
        self.code = waapuro_code

    def loads(self):
        pattern = r'\[([a-zA-Z]+)\s+tag="([^"]+)"\](.*?)\[/\1\]'
        matches = re.findall(pattern, self.code)

        result = []
        for tag_name, _, content in matches:
            nested_data = self.__parse_custom_tags(content)
            result.append({'tag_name': tag_name, 'content': nested_data or content})

        return result

    def __parse_custom_tags(self, text):
        pattern = r'\[([a-zA-Z]+)\s+tag="([^"]+)"\](.*?)\[/\1\]'
        matches = re.findall(pattern, text)

        result = []
        for tag_name, _, content in matches:
            nested_data = self.__parse_custom_tags(content)
            result.append({'tag_name': tag_name, 'content': nested_data or content})

        return result

    def to_html(self, obj=None, tag_mapping=None):
        """

        """


if __name__ == '__main__':
    sample_text = r'[div tag="tag2"]content2[p tag="tag1"]content1[span tag="tag3"]nested content[/span][/p][/div]'
    parser = Waapuro2HTML(sample_text)

    print("Waapuro code object", parser.loads())
    print("Waapuro code object", parser.loads())
