import logging
import logging.config
import os
import sys
from configparser import ConfigParser, NoOptionError, NoSectionError


class ConfigProvider:
    def __init__(self):
        self.logger = logging.getLogger('ConfigProvider')
        self.config_parser = ConfigParser()
        if not os.path.isfile(sys.argv[1]):
            print("Wrong app config file path.")
            sys.exit(1)
        self.config_parser.read(sys.argv[1])
        self.logger.info("Config Provider Initialized")

    def get_config_value(self, section, key):
        try:
            value = self.config_parser.get(section=section, option=key)
            self.logger.debug(f"Getting section {section}. Value of key {key}")
            return value
        except (NoSectionError, NoOptionError):
            self.logger.error("Cannot get key or section from settings")


config_provider = ConfigProvider()
