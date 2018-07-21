#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='spdown',
    version='0.0.5',
    author='Berke Emrecan Arslan',
    author_email='berke@beremaran.com',
    description='Download Spotify playlists from YouTube',
    keywords='youtube spotify spotify-api spotify-playlist',
    url='https://github.com/beremaran/spdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'youtube-dl',
        'google-api-python-client',
        'google-auth',
        'spotipy',
        'eyed3'
    ],
    scripts=[
        'bin/spdown'
    ]
)
