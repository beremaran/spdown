#!/usr/bin/env python


class Track:
    spotify_id: str
    artist: str
    title: str
    youtube_id: str

    def __init__(self):
        pass

    def to_dict(self) -> dict:
        pass

    def __str__(self):
        return '{} - {}'.format(
            self.artist, self.title
        )

    def __repr__(self):
        return self.__str__()
