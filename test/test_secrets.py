#!/usr/bin/env python

import os
import json
import unittest
from collections import OrderedDict

from spdown.secrets import Secrets

TEST_SECRET_PATHS = OrderedDict([
    ('local', 'secrets.json'),
    ('home', os.path.join(
        os.path.expanduser('~'), '.config',
        'spdown', 'secrets'
    ))
])

TEST_SECRETS = {
    'spotify': {
        'username': 'spotify_username',
        'client_id': 'spotify_client_id',
        'client_secret': 'spotify_client_secret'
    },
    'youtube': {
        'developer_key': 'youtube_developer_key'
    }
}


class TestSecrets(unittest.TestCase):
    @staticmethod
    def get_backup_path(secrets_location):
        return '{}.bak'.format(
            TEST_SECRET_PATHS[secrets_location]
        )

    @staticmethod
    def backup(secrets_location):
        backup_path = TestSecrets.get_backup_path(secrets_location)

        if os.path.exists(TEST_SECRET_PATHS[secrets_location]):
            os.rename(
                TEST_SECRET_PATHS[secrets_location],
                backup_path
            )

    @staticmethod
    def restore(secrets_location):
        backup_path = TestSecrets.get_backup_path(secrets_location)

        if os.path.exists(backup_path):
            os.rename(
                backup_path,
                TEST_SECRET_PATHS[secrets_location]
            )

    @staticmethod
    def create_test_secrets(secrets_location):
        TestSecrets.backup(secrets_location)

        with open(TEST_SECRET_PATHS[secrets_location], 'w') as f:
            json.dump(TEST_SECRETS, f)

    def test_find_secret_file(self):
        secrets = Secrets()

        for secret_file in TEST_SECRET_PATHS.keys():
            TestSecrets.backup(secret_file)

        for secret_file in TEST_SECRET_PATHS.keys():
            secrets.set_secret_file(None)
            TestSecrets.create_test_secrets(secret_file)
            secrets._load()
            TestSecrets.restore(secret_file)
            self.assertEqual(TEST_SECRETS, secrets._secrets)

    def test_get_spotify_credentials(self):
        secrets = Secrets()

        TestSecrets.backup('home')
        TestSecrets.create_test_secrets('home')
        secrets.set_secret_file(TEST_SECRET_PATHS['home'])
        client_id, client_secret = secrets.get_spotify_credentials()
        TestSecrets.restore('home')

        self.assertEqual(client_id, TEST_SECRETS['spotify']['client_id'])
        self.assertEqual(client_secret, TEST_SECRETS['spotify']['client_secret'])

    def test_get_spotify_username(self):
        secrets = Secrets()

        TestSecrets.backup('home')
        TestSecrets.create_test_secrets('home')
        secrets.set_secret_file(TEST_SECRET_PATHS['home'])
        username = secrets.get_spotify_username()
        TestSecrets.restore('home')

        self.assertEqual(username, TEST_SECRETS['spotify']['username'])

    def test_get_youtube_dev_key(self):
        secrets = Secrets()

        TestSecrets.backup('home')
        TestSecrets.create_test_secrets('home')
        secrets.set_secret_file(TEST_SECRET_PATHS['home'])
        dev_key = secrets.get_youtube_dev_key()
        TestSecrets.restore('home')

        self.assertEqual(dev_key, TEST_SECRETS['youtube']['developer_key'])


if __name__ == "__main__":
    unittest.main()
