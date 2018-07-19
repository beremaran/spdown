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

import multiprocessing
import os

import eyed3
import youtube_dl
from googleapiclient.discovery import build

from spdown.config import Config
from spdown.secrets import Secrets
from spdown.track import Track

BASE_YOUTUBE_URL = 'https://www.youtube.com/watch?v={}'


class YoutubeLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class Youtube:
    _developer_key: str
    _service = None

    def __init__(self):
        self._developer_key = Secrets.get_youtube_dev_key()
        self._service = build('youtube', 'v3', developerKey=self._developer_key)

    def search_track(self, track: Track) -> dict:
        track_title = str(track)
        print('Searching', track_title, '...')
        results = self._service.search().list(
            maxResults='1',
            q=track_title,
            part='id,snippet'
        ).execute()

        try:
            return results['items'][0]
        except IndexError:
            return {}

    def modify_tracks(self, tracks: list) -> list:
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        modified_tracks = pool.map(self.modify_track, tracks)
        return modified_tracks

    def modify_track(self, track: Track) -> Track:
        search_result = self.search_track(track)
        try:
            track.youtube_id = search_result['id']['videoId']
        except KeyError:
            print('Can\'t find video for track:', str(track))
            track.youtube_id = None

        return track

    def _get_ytdl_options(self, filename):
        download_directory = Config.get('download_directory')

        filename = filename.replace('/', '-')
        filename = os.path.join(download_directory, filename + '.%(ext)s')

        if not os.path.exists(download_directory):
            os.mkdir(download_directory)

        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'logger': YoutubeLogger(),
            'outtmpl': filename
        }

    def _download_track_packed(self, args):
        self.download_track(*args)

    def download_track(self, track: Track, playlist_name: str = None):
        if track.youtube_id is None:
            print('No youtube ID for track', str(track), '!')
            return

        ytdl_options = self._get_ytdl_options(str(track))
        if playlist_name is not None:
            directory = playlist_name.lower()
            directory = directory.replace(' ', '_')
            directory = directory.replace('-', '')
            directory = directory.replace(':', '')

            outtmpl = ytdl_options['outtmpl']
            outtmpl = outtmpl.split('/')
            outtmpl.insert(-1, directory)
            ytdl_options['outtmpl'] = '/'.join(outtmpl)

        ytdl = youtube_dl.YoutubeDL(ytdl_options)

        print('Downloading {} ...'.format(str(track)))

        ytdl.download([
            BASE_YOUTUBE_URL.format(track.youtube_id)
        ])

        # update tags
        mp3 = eyed3.load(ytdl_options['outtmpl'].replace('%(ext)s', 'mp3'))
        mp3.tag.artist = track.artist
        mp3.tag.title = track.title
        mp3.tag.album = track.album_name
        mp3.tag.album_artist = track.artist
        mp3.tag.save()

    def download_tracks(self, tracks: list, playlist_name: str = None):
        thread_arguments = [
            (t, playlist_name)
            for t in tracks
        ]

        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        pool.map(self._download_track_packed, thread_arguments)
