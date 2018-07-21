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

from __future__ import print_function

import argparse
import logging
import sys

from spdown.spotify import Spotify
from spdown.youtube import Youtube

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='spdown',
                                     description='Downloads public Spotify playlists from YouTube')

    parser.add_argument('spotify_uri',
                        type=str,
                        help='Spotify Playlist URI to download')

    parser.add_argument('--config',
                        type=str,
                        required=False,
                        help='Configuration File')

    parser.add_argument('--secrets',
                        type=str,
                        required=False,
                        help='Spotify and Youtube API Secrets File')

    args = parser.parse_args()

    spotify_uri = args.spotify_uri
    configuration_file = args.config
    secrets_file = args.secrets

    spotify_uri = spotify_uri.split(',')
    spotify_uri = [
        uri.strip()
        for uri in spotify_uri
    ]

    for uri in spotify_uri:
        if ':' not in uri:
            sys.stderr.write('Corrupt Spotify URI Format! ({})\n'.format(uri))
            exit(1)

        uri_tokens = uri.split(':')
        if 'playlist' != uri_tokens[-2]:
            sys.stderr.write('A Spotify Playlist URI is required!\n')
            sys.stderr.write('Given type: {}\n'.format(uri_tokens[-2]))
            exit(2)

    spotify = Spotify(secrets_file)
    youtube = Youtube(configuration_file)

    for uri in spotify_uri:
        print('Extracting spotify tracks ...')
        tracks, playlist_name = spotify.extract_tracks(uri)
        print('Searching tracks on YouTube ...')
        tracks = youtube.modify_tracks(tracks)
        print('Downloading tracks from YouTube ...')
        youtube.download_tracks(tracks)
