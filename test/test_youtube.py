#!/usr/bin/env python
import os
import unittest
import logging

from spdown.track import Track
from spdown.youtube import Youtube

TEST_TITLE = 'The Pretender'
TEST_ARTIST = 'Foo Fighters'
TEST_ALBUM = 'Echoes, Silence, Patience & Grace'
TEST_YOUTUBE_ID = 'SBjQ9tuuTJQ'

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


class TestYoutube(unittest.TestCase):
    def test_search_track(self):
        youtube = Youtube()

        track = Track()
        track.title = TEST_TITLE
        track.artist = TEST_ARTIST
        track.album_name = TEST_ALBUM

        result = youtube.search_track(track)
        self.assertEqual(result['id']['videoId'], TEST_YOUTUBE_ID)

    def test_modify_track(self):
        youtube = Youtube()

        track = Track()
        track.title = TEST_TITLE
        track.artist = TEST_ARTIST
        track.album_name = TEST_ALBUM

        track = youtube.modify_track(track)
        self.assertEqual(track.youtube_id, TEST_YOUTUBE_ID)

    def test_download_track(self):
        youtube = Youtube()

        track = Track()
        track.title = TEST_TITLE
        track.artist = TEST_ARTIST
        track.album_name = TEST_ALBUM
        track = youtube.modify_track(track)

        file_path = youtube.download_track(track)
        self.assertTrue(os.path.exists(file_path))


if __name__ == "__main__":
    unittest.main()
