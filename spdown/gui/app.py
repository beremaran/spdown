#!/usr/bin/env python
from kivy.adapters.listadapter import ListAdapter
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton
from kivy.uix.scrollview import ScrollView

from spdown.db import Artist, session, Playlist, Album
from spdown.gui.listview import SPListView
from spdown.gui.treeview import SPTreeView, SPTreeNode


class SPDown(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.navigator = None
        self.track_navigator = None

    def build(self):
        horizontal_box = BoxLayout(orientation='horizontal')
        vertical_box_right = BoxLayout(orientation='vertical')
        vertical_box_left = BoxLayout(orientation='vertical',
                                      size_hint=(.4, 1))

        vertical_box_left.add_widget(Label(text='Library',
                                           size_hint=(1, .1)))
        vertical_box_left.add_widget(self.build_navigator())
        horizontal_box.add_widget(vertical_box_left)

        vertical_box_right.add_widget(Label(text='Playlists', size_hint=(1, .1)))
        vertical_box_right.add_widget(self.build_track_navigator())

        horizontal_box.add_widget(vertical_box_right)

        self.populate_navigator()
        self.navigator.add_click_handler(self._navigator_click_handler)

        return horizontal_box

    def build_navigator(self):
        scroll = ScrollView(pos=(0, 0), size_hint=(1, 0.9))
        nav = SPTreeView(hide_root=True, size_hint=(1, None))
        nav.bind(minimum_height=nav.setter('height'))

        scroll.add_widget(nav)
        self.navigator = nav
        return scroll

    def build_track_navigator(self):
        scroll = ScrollView(pos=(0, 0), size_hint=(1, 1))
        nav = SPListView(size_hint=(1, 1))

        scroll.add_widget(nav)
        self.track_navigator = nav
        return scroll

    def _navigator_click_handler(self, node):
        self.populate_tracks(node.spotify_type, node.spotify_id)

    def populate_navigator(self):
        for node in self.navigator.iterate_all_nodes():
            self.navigator.remove_node(node)

        n_playlists = self.navigator.add_node(SPTreeNode(text='Playlists'))
        n_artists = self.navigator.add_node(SPTreeNode(text='Artists'))

        # populate artists
        artists = session.query(Artist).all()
        for artist in artists:
            n_artist = self.navigator.add_node(SPTreeNode(text=artist.name,
                                                          spotify_type='artist',
                                                          spotify_id=artist.spotify_id),
                                               n_artists)

            albums = artist.albums
            for album in albums:
                self.navigator.add_node(SPTreeNode(text=album.title,
                                                   spotify_id=album.spotify_id,
                                                   spotify_type='album'), n_artist)

        # populate playlists
        playlists = session.query(Playlist).all()
        for playlist in playlists:
            self.navigator.add_node(SPTreeNode(text=playlist.name,
                                               spotify_id=playlist.spotify_id,
                                               spotify_type='playlist'), n_playlists)

    def populate_tracks(self, spotify_type: str, spotify_id: str):
        data = None
        if spotify_type == 'artist':
            data = session.query(Artist).filter_by(spotify_id=spotify_id).first()
        if spotify_type == 'album':
            data = session.query(Album).filter_by(spotify_id=spotify_id).first()
        if spotify_type == 'playlist':
            data = session.query(Playlist).filter_by(spotify_id=spotify_id).first()

        if data is None:
            return

        data = data.tracks
        data = [
            {'text': track.name,
             'is_selected': False}
            for track in data
        ]

        args_converter = lambda row_index, rec: {'text': rec['text'],
                                                 'size_hint_y': None,
                                                 'height': 25}

        list_adapter = ListAdapter(data=data,
                                   args_converter=args_converter,
                                   cls=ListItemButton,
                                   selection_mode='single',
                                   allow_empty_selection=False)

        self.track_navigator.adapter = list_adapter
