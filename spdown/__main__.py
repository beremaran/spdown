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

from spdown.db import session, Track, Artist
from spdown.spotify import Spotify
from spdown.youtube import Youtube

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


def download_objects(options):
    spotify_uri = options.command_options
    if len(spotify_uri) == 1:
        spotify_uri = spotify_uri[0]

    configuration_file = options.config
    secrets_file = options.secrets

    spotify_uri = spotify_uri.split(',')
    spotify_uri = [
        uri.strip()
        for uri in spotify_uri
    ]

    for uri in spotify_uri:
        if ':' not in uri:
            sys.stderr.write('Corrupt Spotify URI Format! ({})\n'.format(uri))
            exit(1)

    spotify = Spotify(secrets_file)
    youtube = Youtube(configuration_file)

    for uri in spotify_uri:
        spotify.import_object(uri)

        # fetch not downloaded tracks and download them
        tracks = session.query(Track).filter_by(download=True, file_path=None).all()
        tracks = youtube.modify_tracks(tracks)

        youtube.download_tracks(tracks)


def dump_library():
    artists = session.query(Artist).order_by('name').all()
    for i, artist in enumerate(artists):
        print('{:3d}) {}'.format(i + 1, artist.name))
        for j, album in enumerate(artist.albums):
            print('\t{:3d}) {}'.format(j + 1, album.title))
            for k, track in enumerate(album.tracks):
                print('\t\t{:3d}) {}'.format(k + 1, track.name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='spdown',
                                     description='Downloads public Spotify playlists from YouTube')

    parser.add_argument('command',
                        type=str,
                        choices=(
                            'download', 'dump_library'
                        ),
                        help='Spotify Playlist URI to download')

    parser.add_argument('command_options',
                        type=str,
                        nargs='*')

    parser.add_argument('--config',
                        type=str,
                        required=False,
                        help='Configuration File')

    parser.add_argument('--secrets',
                        type=str,
                        required=False,
                        help='Spotify and Youtube API Secrets File')

    args = parser.parse_args()

    if args.command == 'download':
        download_objects(args)
    if args.command == 'dump_library':
        dump_library()
