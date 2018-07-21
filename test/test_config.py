#!/usr/bin/env python
import os
import json
import unittest
from collections import OrderedDict

from spdown.config import Config

TEST_CONFIG_PATHS = OrderedDict([
    ('local', 'config.json'),
    ('home', os.path.join(
        os.path.expanduser('~'), '.config',
        'spdown', 'config'
    ))
])

TEST_CONFIG = {
    'download_directory': '~/TestMusic'
}


class TestConfig(unittest.TestCase):
    @staticmethod
    def get_backup_path(config_location):
        return '{}.bak'.format(
            TEST_CONFIG_PATHS[config_location]
        )

    @staticmethod
    def backup_configuration(config_location):
        backup_path = TestConfig.get_backup_path(config_location)

        if os.path.exists(TEST_CONFIG_PATHS[config_location]):
            os.rename(
                TEST_CONFIG_PATHS[config_location],
                backup_path
            )

    @staticmethod
    def restore_configuration(config_location):
        backup_path = TestConfig.get_backup_path(config_location)

        if os.path.exists(backup_path):
            os.rename(
                backup_path,
                TEST_CONFIG_PATHS[config_location]
            )

    @staticmethod
    def create_test_config(config_location):
        TestConfig.backup_configuration(config_location)

        with open(TEST_CONFIG_PATHS[config_location], 'w') as f:
            json.dump(TEST_CONFIG, f)

    def test_find_configuration_file(self):
        config = Config()

        for config_path in TEST_CONFIG_PATHS.keys():
            TestConfig.backup_configuration(config_path)

        for config_path in TEST_CONFIG_PATHS.keys():
            config.set_config_path(None)
            TestConfig.create_test_config(config_path)
            config._load(exit_on_error=False)
            TestConfig.restore_configuration(config_path)
            self.assertEqual(TEST_CONFIG, config._configuration)

    def test_get(self):
        config = Config()

        for config_path in TEST_CONFIG_PATHS.keys():
            TestConfig.backup_configuration(config_path)

        for config_path in TEST_CONFIG_PATHS.keys():
            config.set_config_path(None)
            TestConfig.create_test_config(config_path)
            download_directory = config.get('download_directory')
            TestConfig.restore_configuration(config_path)
            self.assertEqual(download_directory, TEST_CONFIG['download_directory'])

    def test_set(self):
        config = Config()

        for config_path in TEST_CONFIG_PATHS.keys():
            TestConfig.backup_configuration(config_path)

        for config_path in TEST_CONFIG_PATHS.keys():
            config.set_config_path(None)
            TestConfig.create_test_config(config_path)
            config.set('download_directory', 'test')
            TestConfig.restore_configuration(config_path)
            self.assertEqual(config.get('download_directory'), 'test')

    def test_fix_path_errors(self):
        config = Config()

        for config_path in TEST_CONFIG_PATHS.keys():
            TestConfig.backup_configuration(config_path)

        for config_path in TEST_CONFIG_PATHS.keys():
            config.set_config_path(None)
            TestConfig.create_test_config(config_path)
            config.set('download_directory', '~/Music/')
            config._configuration = None
            self.assertEqual(config.get('download_directory'), '~/Music')
            TestConfig.restore_configuration(config_path)


if __name__ == "__main__":
    unittest.main()
