import os
import json

from waapuro import settings


def installed_templates(base_dir, interface_dir):
    result = []
    for item in os.listdir(interface_dir):
        item_path = os.path.join(interface_dir, item)
        if os.path.isdir(item_path):
            template_config = os.path.join(item_path, "config.json")
            if os.path.exists(template_config):
                with open(template_config, 'r', encoding=settings.CHARSET) as config_file:
                    config_data = json.load(config_file)
                    template_dir = os.path.join(base_dir, item_path)
                    config_data['DIRS'] = [template_dir]
                    result.append(config_data)
    return result
