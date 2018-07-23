#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Genre - Artist Association Table
genre_artist_table = Table(
    'genres_artists', Base.metadata,
    Column('genre_id', Integer, ForeignKey('genres.id')),
    Column('artist_id', Integer, ForeignKey('artists.id'))
)

# Genre - Album Association Table
genre_album_table = Table(
    'genres_albums', Base.metadata,
    Column('genre_id', Integer, ForeignKey('genres.id')),
    Column('album_id', Integer, ForeignKey('albums.id'))
)

# Artist - Album Association Table
artist_album_table = Table(
    'artists_albums', Base.metadata,
    Column('artist_id', Integer, ForeignKey('artists.id')),
    Column('album_id', Integer, ForeignKey('albums.id'))
)

# Artist - Track Association Table
artist_track_table = Table(
    'artists_tracks', Base.metadata,
    Column('artist_id', Integer, ForeignKey('artists.id')),
    Column('track_id', Integer, ForeignKey('tracks.id'))
)

# Album - Track Association Table
album_track_table = Table(
    'albums_tracks', Base.metadata,
    Column('album_id', Integer, ForeignKey('albums.id')),
    Column('track_id', Integer, ForeignKey('tracks.id'))
)

# Track - Playlist Association Table
track_playlist_table = Table(
    'tracks_playlists', Base.metadata,
    Column('track_id', Integer, ForeignKey('tracks.id')),
    Column('playlist_id', Integer, ForeignKey('playlists.id'))
)


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    spotify_id = Column(String)

    name = Column(String)
    tracks = relationship('Track',
                          secondary=track_playlist_table)


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    artists = relationship('Artist',
                           back_populates='genres',
                           secondary=genre_artist_table)
    albums = relationship('Album',
                          back_populates='genres',
                          secondary=genre_album_table)


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    spotify_id = Column(String)

    name = Column(String)
    image = Column(String)
    genres = relationship('Genre',
                          back_populates='artists',
                          secondary=genre_artist_table)
    albums = relationship('Album',
                          back_populates='artists',
                          secondary=artist_album_table)
    tracks = relationship('Track',
                          back_populates='artists',
                          secondary=artist_track_table)


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    spotify_id = Column(String)

    title = Column(String)
    album_type = Column(String)  # album, single or compilation
    artists = relationship('Artist',
                           back_populates='albums',
                           secondary=artist_album_table)
    cover_art = Column(String)
    tracks = relationship('Track',
                          secondary=album_track_table)
    genres = relationship('Genre',
                          back_populates='albums',
                          secondary=genre_album_table)


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    youtube_id = Column(String)
    spotify_id = Column(String)

    name = Column(String)
    album = relationship('Album',
                         back_populates='tracks',
                         secondary=album_track_table)
    artists = relationship('Artist',
                           back_populates='tracks',
                           secondary=artist_track_table)
    disc_number = Column(Integer)
    track_number = Column(Integer)

    playlists = relationship('Playlist',
                             back_populates='tracks',
                             secondary=track_playlist_table)