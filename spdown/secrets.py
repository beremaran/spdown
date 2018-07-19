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


class Secrets:
    _secret_file: str = None
    _secrets: dict = None

    @staticmethod
    def set_secret_file(path):
        Secrets._secret_file = path

    @staticmethod
    def _find_secret_file():
        if os.path.exists('secrets.json'):
            Secrets._secret_file = 'secrets.json'
            return

        Secrets._secret_file = None

    @staticmethod
    def _load():
        if Secrets._secret_file is None:
            Secrets._find_secret_file()
        if Secrets._secrets is None:
            with open(Secrets._secret_file, 'r') as f:
                Secrets._secrets = json.load(f)

    @staticmethod
    def get_spotify_credentials() -> tuple:
        Secrets._load()
        spotify_secrets = Secrets._secrets['spotify']
        return spotify_secrets['client_id'], spotify_secrets['client_secret']

    @staticmethod
    def get_spotify_username() -> str:
        Secrets._load()
        if 'username' in Secrets._secrets['spotify'].keys():
            return Secrets._secrets['spotify']['username']
        else:
            return ''

    @staticmethod
    def get_youtube_dev_key() -> str:
        Secrets._load()
        return Secrets._secrets['youtube']['developer_key']
