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
import sys
import json
from collections import OrderedDict

from spdown.config import is_empty

SECRET_PATHS = OrderedDict([
    ('local', 'secrets.json'),
    ('home', os.path.join(
        os.path.expanduser('~'), '.config',
        'spdown', 'secrets'
    ))
])


class Secrets:
    def __init__(self, secret_file: str = None, secrets: dict = None):
        self._secret_file = secret_file
        self._secrets = secrets

    def set_secret_file(self, path):
        self._secret_file = path

    def _find_secret_file(self):
        self._secret_file = None

        for secrets_path in SECRET_PATHS.values():
            if os.path.exists(secrets_path):
                self._secret_file = secrets_path

        return self._secret_file is not None

    @staticmethod
    def _warn_user_to_fill_secrets():
        sys.stderr.write(
            'Please fill your Spotify and YouTube secrets in {}\n'.format(
                SECRET_PATHS['home']
            )
        )

        exit(0)

    def _load(self):
        if self._secret_file is None:
            result = self._find_secret_file()
            if not result:
                os.makedirs(
                    os.path.sep.join(SECRET_PATHS['home'].split(os.path.sep)[:-1])
                )

                self._secret_file = SECRET_PATHS['home']
                self._secrets = {
                    'spotify': {
                        'username': '',
                        'client_id': '',
                        'client_secret': ''
                    },
                    'youtube': {
                        'developer_key': ''
                    }
                }

                self._save()
                self._warn_user_to_fill_secrets()

        if self._secrets is None:
            with open(self._secret_file, 'r') as f:
                self._secrets = json.load(f)

            if is_empty(self._secrets['spotify']['client_id']):
                self._warn_user_to_fill_secrets()
            if is_empty(self._secrets['spotify']['client_secret']):
                self._warn_user_to_fill_secrets()
            if is_empty(self._secrets['youtube']['developer_key']):
                self._warn_user_to_fill_secrets()

    def _save(self):
        if self._secret_file is None:
            self._find_secret_file()

        with open(self._secret_file, 'w') as f:
            json.dump(self._secrets, f, indent=4)

    def get_spotify_credentials(self) -> tuple:
        self._load()
        spotify_secrets = self._secrets['spotify']
        return spotify_secrets['client_id'], spotify_secrets['client_secret']

    def get_spotify_username(self) -> str:
        self._load()
        if 'username' in self._secrets['spotify'].keys():
            return self._secrets['spotify']['username']
        else:
            return ''

    def get_youtube_dev_key(self) -> str:
        self._load()
        return self._secrets['youtube']['developer_key']
