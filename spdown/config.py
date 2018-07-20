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

import json
import os
import sys
from collections import OrderedDict

CONFIG_PATHS = OrderedDict([
    ('local', 'config.json'),
    ('home', os.path.join(
        os.path.expanduser('~'), '.config',
        'spdown', 'config'
    ))
])


class Config:
    _config_path: str
    _configuration: dict

    def __init__(self, config_path: str = None, configuration: dict = None):
        self._config_path = config_path
        self._configuration = configuration

    def set_config_path(self, path):
        self._config_path = path

    def _find_configuration_file(self) -> bool:
        self._config_path = None

        for config_path in CONFIG_PATHS.values():
            if os.path.exists(config_path):
                self._config_path = config_path

        return self._config_path is not None

    def _load(self):
        if self._configuration is not None:
            return

        if self._config_path is None:
            result = self._find_configuration_file()
            if not result:
                os.makedirs(
                    os.path.sep.join(CONFIG_PATHS['home'].split(os.path.sep)[:-1])
                )

                self._config_path = CONFIG_PATHS['home']
                self._configuration = {
                    'download_directory': os.path.join(
                        os.path.expanduser('~'), 'Music'
                    )
                }
                self._save()

                sys.stderr.write(
                    'Please fill your configuration in {}\n'.format(
                        CONFIG_PATHS['home']
                    )
                )

                exit(0)

        if self._configuration is None:
            with open(self._config_path, 'r') as f:
                self._configuration = json.load(f)

            self._fix_path_errors()

    def _fix_path_errors(self):
        config = self._configuration
        download_directory = config['download_directory']

        if download_directory[-1] == os.path.sep:
            download_directory = download_directory[:-1]
            config['download_directory'] = download_directory

            self._configuration = config
            self._save()

    def _save(self):
        if self._config_path is None:
            self._find_configuration_file()

        with open(self._config_path, 'w') as f:
            json.dump(self._configuration, f, indent=4)

    def get(self, key) -> any:
        self._load()

        if key not in self._configuration.keys():
            return None

        return self._configuration[key]

    def set(self, key, value):
        self._load()
        self._configuration[key] = value
        self._save()
