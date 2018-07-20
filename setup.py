#!/usr/bin/env python

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='spdown',
    version='0.0.1',
    author='Berke Emrecan Arslan',
    author_email='berke@beremaran.com',
    description='Download Spotify playlists from YouTube',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/beremaran/spdown',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    )
)
