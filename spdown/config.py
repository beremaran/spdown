#!/usr/bin/env python

import os
import json
from json import JSONDecodeError


class Config:
    _config_path: str = None
    _configuration: dict = None

    def __init__(self):
        pass

    @staticmethod
    def set_config_path(path):
        Config._config_path = path

    @staticmethod
    def _find_configuration_file():
        if os.path.exists('config.json'):
            Config._config_path = 'config.json'

    @staticmethod
    def _load():
        if Config._config_path is None:
            Config._find_configuration_file()
        if Config._configuration is None:
            retry = True
            while retry:
                retry = False

                try:
                    with open(Config._config_path, 'r') as f:
                        Config._configuration = json.load(f)
                except JSONDecodeError:
                    retry = True

            Config._fix_path_errors()

    @staticmethod
    def _fix_path_errors():
        config = Config._configuration
        download_directory = config['download_directory']

        if download_directory[-1] == '/':
            download_directory = download_directory[:-1]
            config['download_directory'] = download_directory

        Config._configuration = config
        Config._save()

    @staticmethod
    def _save():
        if Config._config_path is None:
            Config._find_configuration_file()

        with open(Config._config_path, 'w') as f:
            json.dump(Config._configuration, f, indent=4)

    @staticmethod
    def get(key) -> any:
        Config._load()

        if key not in Config._configuration.keys():
            return None

        return Config._configuration[key]

    @staticmethod
    def set(key, value):
        Config._load()
        Config._configuration[key] = value
        Config._save()
