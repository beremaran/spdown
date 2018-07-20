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

import spotipy
from spdown.youtube import FILENAME_ILLEGAL_CHARS
from spotipy.oauth2 import SpotifyClientCredentials

from spdown.secrets import Secrets
from spdown.track import Track


class Spotify:
    def __init__(self, secrets_path: str = None):
        self._secrets = Secrets(secrets_path)

        client_id, client_secret = self._secrets.get_spotify_credentials()
        self._credentials = SpotifyClientCredentials(client_id=client_id,
                                                     client_secret=client_secret)
        self._client = spotipy.Spotify(client_credentials_manager=self._credentials)

    def extract_tracks(self, playlist_id: str) -> tuple:
        tracks_final = []
        username = self._secrets.get_spotify_username()

        if ':' in playlist_id:
            playlist_id = playlist_id.split(':')[-1]

        results = self._client.user_playlist(username, playlist_id, 'tracks,next,name')
        tracks = results['tracks']

        tracks_final.extend(
            self._extract_tracks_from_resultset(tracks)
        )
        while tracks['next']:
            tracks = self._client.next(tracks)
            tracks_final.extend(
                self._extract_tracks_from_resultset(tracks)
            )

        playlist_name = results['name']

        return tuple(tracks_final), playlist_name

    def _extract_tracks_from_resultset(self, tracks):
        tracks_list = []

        for item in tracks['items']:
            tracks_list.append(self._extract_track(item['track']))

        return tracks_list

    @staticmethod
    def _extract_track(track) -> Track:
        _track = Track()

        _track.artist = track['artists'][0]['name']
        _track.title = track['name']
        _track.spotify_id = track['id']
        _track.album_name = track['album']['name']

        # remove trailing dots
        while _track.artist[-1] in FILENAME_ILLEGAL_CHARS:
            _track.artist = _track.artist[:-1]
        while _track.title[-1] in FILENAME_ILLEGAL_CHARS:
            _track.title = _track.title[:-1]
        # remove illegal characters from album names
        for illegal_char in FILENAME_ILLEGAL_CHARS:
            _track.album_name = _track.album_name.replace(illegal_char, '')

        return _track
