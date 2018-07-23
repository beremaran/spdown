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

import multiprocessing
import os
import re
import sys
from uuid import uuid4

import eyed3
import youtube_dl
from googleapiclient.discovery import build

from spdown.config import Config
from spdown.db import session
from spdown.secrets import Secrets
from spdown.db.models import Track

NON_ALPHANUM_PATTERN = re.compile('[\W_]+', re.UNICODE)
BASE_YOUTUBE_URL = 'https://www.youtube.com/watch?v={}'
FILENAME_ILLEGAL_CHARS = ['[', ']', '"', '/', ':', '?']


class YoutubeLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class Youtube:
    def __init__(self, configuration_path: str = None, secrets_path: str = None):
        self._secrets = Secrets(secrets_path)
        self._config = Config(configuration_path)

        self._developer_key = self._secrets.get_youtube_dev_key()
        self._service = build('youtube', 'v3', developerKey=self._developer_key)

    def search_track(self, track: Track) -> dict:
        track_title = '{} - {}'.format(track.artists[0].name, track.name)
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
            youtube_id = search_result['id']['videoId']
        except KeyError:
            print('Can\'t find video for track:', str(track))
            youtube_id = None

        session.query(Track).filter_by(id=track.id).update({
            'youtube_id': youtube_id
        })
        session.commit()

        track = session.query(Track).filter_by(id=track.id).first()
        return track

    def _get_ytdl_options(self, track: Track):
        download_directory = self._config.get('download_directory')
        filename = '{}/{}/{}.%(ext)s'.format(
            track.artists[0].name.replace('/', ''),
            track.album[0].title.replace('/', ''),
            uuid4()
        )

        filename = os.path.join(download_directory, filename)

        if not os.path.exists(download_directory):
            os.mkdir(download_directory)

        return {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'add-metadata': True,
            'logger': YoutubeLogger(),
            'outtmpl': filename
        }

    @staticmethod
    def _exists(path):
        return os.path.exists(path) and os.stat(path).st_size > 0

    def download_track(self, track: Track):
        if track.youtube_id is None:
            print('No youtube ID for track', str(track), '!')
            return

        ytdl_options = self._get_ytdl_options(track)

        # create directories

        if track.file_path is not None:
            print('Skipping already downloaded file ...')
            return

        ytdl = youtube_dl.YoutubeDL(ytdl_options)

        print('Downloading {} ...'.format(str(track)))

        ytdl.download([
            BASE_YOUTUBE_URL.format(track.youtube_id)
        ])

        print('Tagging {} ...'.format(str(track)))

        # update tags
        mp3_path = ytdl_options['outtmpl'].replace('%(ext)s', 'mp3')
        mp3 = eyed3.load(mp3_path)
        if mp3 is None:
            sys.stderr.write('Can\'t open downloaded file for tagging: {}\n'.format(mp3_path))
            sys.stderr.write('Falling back to manual tag initializing\n')
            mp3 = eyed3.mp3.Mp3AudioFile(mp3_path)
            mp3.initTag(version=eyed3.id3.ID3_V2_3)

        mp3.tag.artist = track.artists[0].name
        mp3.tag.title = track.name
        mp3.tag.album = track.album[0].title
        mp3.tag.album_artist = track.artists[0].name
        mp3.tag.disc_num = 1

        if len(track.album) > 0:
            album = track.album[0]
            if len(album.genres) > 0:
                mp3.tag.genre = album.genres[0].name
            else:
                artist = track.artists[0]
                if len(artist.genres) > 0:
                    mp3.tag.genre = artist.genres[0].name

        mp3.tag.save()

        path_tokens = mp3_path.split(os.path.sep)
        filename = '{}.mp3'.format(
            ' - '.join([
                track.artists[0].name, track.name
            ])
        ).replace('/', '')
        path_tokens[-1] = filename
        new_path = os.path.sep.join(path_tokens)

        if os.path.exists(new_path):
            os.remove(new_path)

        os.rename(mp3_path, new_path)
        session.query(Track).filter_by(id=track.id).update({
            'file_path': new_path,
            'download': False
        })
        session.commit()

        return new_path

    def download_tracks(self, tracks: list):
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        pool.map(self.download_track, tracks)
        pool.close()
        pool.join()
