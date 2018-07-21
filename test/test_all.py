#!/usr/bin/env python

import unittest

test_modules = [
    'test.test_config',
    'test.test_secrets',
    'test.test_spotify',
    'test.test_youtube'
]

if __name__ == "__main__":
    suite = unittest.TestSuite()

    for tm in test_modules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(tm))

    unittest.TextTestRunner().run(test=suite)
