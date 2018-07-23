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

from spdown.db.models import Track as DBTrack
from spdown.db.models import Album

from spdown.db import session, Artist
from spdown.youtube import FILENAME_ILLEGAL_CHARS
from spotipy.oauth2 import SpotifyClientCredentials

from spdown.secrets import Secrets
from spdown.track import Track

from lru import lru_cache_function


class Spotify:
    def __init__(self, secrets_path: str = None):
        self._secrets = Secrets(secrets_path)

        client_id, client_secret = self._secrets.get_spotify_credentials()
        self._credentials = SpotifyClientCredentials(client_id=client_id,
                                                     client_secret=client_secret)
        self._client = spotipy.Spotify(client_credentials_manager=self._credentials)

    def import_object(self, spotify_uri: str):
        tokens = spotify_uri.split(':')
        object_type = tokens[-2]
        spotify_id = tokens[-1]

        if object_type == "playlist":
            self.import_playlist(spotify_id)
        if object_type == "artist":
            self.import_artist(spotify_id)
        if object_type == "album":
            self.import_album(spotify_id)
        if object_type == "track":
            self.import_track(spotify_id)

    def import_playlist(self, spotify_id: str):
        # TODO: check if playlist already exists
        tracks_final = []
        username = self._secrets.get_spotify_username()

        results = self._client.user_playlist(username, spotify_id, 'tracks,next,name')
        tracks = results['tracks']
        tracks_final.extend(tracks)
        while tracks['next']:
            tracks = self._client.next(tracks)
            tracks_final.extend(tracks)

        for track in tracks_final:
            self.import_track(track['id'])

    def import_artist(self, spotify_id: str) -> Artist:
        pass

    def import_album(self, spotify_id: str) -> Album:
        pass

    def import_track(self, spotify_id: str) -> DBTrack:
        db_track = session.query(DBTrack).filter_by(spotify_id=spotify_id).first()
        if db_track is not None:
            return db_track

        track = self._client.track(spotify_id)
        album = self.import_album(track['album']['id'])

        artists = []
        for artist in track['artists']:
            artists.append(artist['id'])

        artists = [
            self.import_artist(artist)
            for artist in artists
        ]

        db_track = DBTrack(spotify_id=spotify_id,
                           name=track['name'],
                           album=[album],
                           artists=artists,
                           disc_number=track['disc_number'],
                           track_number=track['track_number'])

        session.add(db_track)
        session.commit()

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
    @lru_cache_function(max_size=1024, expiration=15 * 60)
    def _extract_artist(spotify_client, artist_id):
        if artist_id is not None:
            genres = spotify_client.artist(artist_id)['genres']
            if len(genres) > 0:
                return genres[0]

        return None

    def _extract_track(self, track) -> Track:
        _track = Track()

        _track.artist = track['artists'][0]['name']
        _track.title = track['name']
        _track.spotify_id = track['id']
        _track.album_name = track['album']['name']

        artist_id = track['artists'][0]['id']
        _track.artist_genre = self._extract_artist(spotify_client=self._client, artist_id=artist_id)

        while len(_track.artist) > 0 and _track.artist[-1] in FILENAME_ILLEGAL_CHARS:
            _track.artist = _track.artist[:-1]
        while len(_track.title) > 0 and _track.title[-1] in FILENAME_ILLEGAL_CHARS:
            _track.title = _track.title[:-1]
        # remove illegal characters from album names
        for illegal_char in FILENAME_ILLEGAL_CHARS:
            _track.album_name = _track.album_name.replace(illegal_char, '')

        return _track
