#!/usr/bin/env python

import sys
import argparse

from spdown.config import Config
from spdown.secrets import Secrets
from spdown.spotify import Spotify
from spdown.youtube import Youtube

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

    Secrets.set_secret_file(secrets_file)
    Config.set_config_path(configuration_file)

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

    spotify = Spotify()
    youtube = Youtube()

    for uri in spotify_uri:
        tracks, playlist_name = spotify.extract_tracks(uri)
        tracks = youtube.modify_tracks(tracks)

        youtube.download_tracks(tracks, playlist_name)
