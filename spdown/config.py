#!/usr/bin/env python
"""
MIT License

Copyright (c) 2018 Berke Emrecan ARSLAN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import json
from json import JSONDecodeError


class Config:
    _config_path : str = None
    _configuration : dict = None

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

                with open(Config._config_path, 'r') as f:
                    Config._configuration = json.load(f)

            Config._fix_path_errors()

    @staticmethod
    def _fix_path_errors():
        config = Config._configuration
        download_directory = config['download_directory']

        if download_directory[-1] == os.path.sep:
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
