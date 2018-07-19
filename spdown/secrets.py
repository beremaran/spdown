#!/usr/bin/env python

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
