#!/usr/bin/env python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from spdown.secrets import Secrets
from spdown.track import Track


class Spotify:
    _credentials: SpotifyClientCredentials
    _client: spotipy.Spotify

    def __init__(self):
        client_id, client_secret = Secrets.get_spotify_credentials()
        self._credentials = SpotifyClientCredentials(client_id=client_id,
                                                     client_secret=client_secret)
        self._client = spotipy.Spotify(client_credentials_manager=self._credentials)

    def extract_tracks(self, playlist_id: str) -> tuple:
        tracks_final = []
        username = Secrets.get_spotify_username()

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

        return _track
