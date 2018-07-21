#!/usr/bin/env python

import unittest

from spdown.spotify import Spotify



class TestSpotifyExtraction(unittest.TestCase):
    def test_track_count(self):
        spotify = Spotify()
        tracks, playlist_name = spotify.extract_tracks('spotify:user:beremaran:playlist:5NB6rw6Up1jL27x3I9jEmS')
        self.assertEqual(len(tracks), 11)

    def test_extract_track(self):
        spotify = Spotify()

        tracks, playlist_name = spotify.extract_tracks(
            'spotify:user:beremaran:playlist:5NB6rw6Up1jL27x3I9jEmS'
        )

        for track in tracks:
            self.assertIsNotNone(track.artist)
            self.assertIsNotNone(track.title)
            self.assertIsNotNone(track.spotify_id)
            self.assertIsNotNone(track.album_name)


if __name__ == "__main__":
    unittest.main()
