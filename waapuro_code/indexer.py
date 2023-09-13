"""
WaapuroCode files indexer
"""
import datetime
import logging
import threading
from pathlib import Path

from django.core.cache import cache
from lxml import etree

from waapuro import settings
import os

from waapuro.publish.models import ArticleUrlWcfMapping, Article
from waapuro_code.tags_mapping import WaapuroCode, generate_field_mapping


class WaapuroIndexer:
    def __init__(self):
        # Initialize the root directories from settings
        self.root_dirs = [self._get_waapuro_root(root_dict) for root_dict in settings.WAAPUROCODE_ROOTS]
        self.root_dir_apps = {
            "datas": "datas/",
            "logs": "logs/",
        }
        # Start Logger
        self._create_logger()
        # create cache buckets
        self.cache_key_filelist = "WaapuroIndexer_Filelist"
        self.files = self._get_or_create_cache(self.cache_key_filelist, [])

    def _get_or_create_cache(self, name, default):
        if cache.get(name) is None:
            cache.set(name, default)
            self.logger.info(f"Cache Bucket Online! '{self.cache_key_filelist}'")
        return cache.get(name)

    @staticmethod
    def _get_waapuro_root(root_dict):
        """
        Get Waapuro files storage location
        """
        if root_dict['server'] == 'LOCAL':
            return Path(os.path.expanduser(root_dict['root']))
        if root_dict['server'] == 'FTP':
            return None
        return None

    def _create_logger(self):
        log_name = "waapurocode_indexer"
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s %(name)s] %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
        console_handler.setFormatter(formatter)

        # make dir
        filename = f"/{log_name}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}.log"
        log_root = self.root_dirs[0]  # default first option

        log_directory = os.path.join(log_root, self.root_dir_apps["logs"])
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        file_handler = logging.FileHandler(
            log_directory + filename
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def search_waapuro_files(self):
        """
        Step.1　Load/Upload file list
        """

        def _thread():
            found_files = []
            # Use rglob to recursively search for files ending with .waapuro in each root directory
            print(self.root_dirs)
            for root_dir in self.root_dirs:
                if root_dir is not None:
                    found = list(root_dir.rglob('*.waapuro'))
                    found_files.extend(found)
                    print(found)
            self.files = found_files
            cache.set(self.cache_key_filelist, self.files)

        thread = threading.Thread(target=_thread)
        thread.start()
        self.logger.info("Started a thread for search *.waapuro.")
        return thread

    def build_index(self):
        """
        Step.2　Build index
        and save to Database
        """

        def _thread():
            flist = cache.get(self.cache_key_filelist)
            self.logger.info(f"{len(flist)} .waapuro file found.")
            # clear old datas
            ArticleUrlWcfMapping.objects.all().delete()
            for path in flist:
                self.logger.debug(f"Creating WaapuroCode obj form '{path}'.")
                # make new datas
                wc = WaapuroCode()
                with open(path, 'r', encoding=settings.CHARSET) as file:
                    wc.set_waapurocode(file.read())
                # import new datas
                profile = wc.get_profile()
                self.logger.debug(profile)
                ArticleUrlWcfMapping(url=profile['url'], wc_path=path).save()

        thread = threading.Thread(target=_thread)
        thread.start()
        self.logger.info("Started a thread for Build Index.")
        return thread

    def collect_profiles(self):
        """
        Step.3　Collect Profiles
        """

        def _thread():
            # clear old datas
            Article.objects.all().delete()

            # load waapuro files index
            index_list = ArticleUrlWcfMapping.objects.all()

            for index in index_list:
                p = index.wc_path
                # url = index.url
                self.logger.debug(f"Reading '{p}'.")

                # read waapuro file
                wc = WaapuroCode()
                with open(p, 'r', encoding=settings.CHARSET) as file:
                    wc.set_waapurocode(file.read())

                # Generate field mappings
                profile = wc.get_profile()
                field_mapping = generate_field_mapping(profile)
                field_mapping["content"] = etree.tostring(
                    wc.get_content(), pretty_print=True,
                    encoding="unicode"
                )

                # Check if content is None or empty
                if not field_mapping["content"]:
                    self.logger.warning(f"{p}Content is empty or None")

                # Save Obj
                Article(**field_mapping).save()

        thread = threading.Thread(target=_thread)
        thread.start()
        self.logger.info("Started a thread for Collect Profiles.")
        return thread

    def flow_build_index(self):
        self.logger.info("FLOW STARTED")
        try:
            self.search_waapuro_files().join()
            self.build_index().join()
            self.collect_profiles().join()
        except Exception as e:
            # 捕捉异常并记录到日志
            self.logger.error("An error occurred: %s", str(e))
