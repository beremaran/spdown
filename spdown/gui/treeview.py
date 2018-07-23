#!/usr/bin/env python
from kivy.uix.treeview import TreeView, TreeViewLabel


class SPTreeView(TreeView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.previous_selected_item = self.selected_node
        self.click_handlers = []

    def add_click_handler(self, handler):
        self.click_handlers.append(handler)

    def on_touch_up(self, touch):
        if self.previous_selected_item != self.selected_node:
            for handler in self.click_handlers:
                handler(self.selected_node)

            self.previous_selected_item = self.selected_node

        return super().on_touch_up(touch)


class SPTreeNode(TreeViewLabel):
    spotify_id: str
    spotify_type: str

    def __init__(self, **kwargs):
        self.spotify_id = None
        self.spotify_type = None

        if 'spotify_id' in kwargs.keys():
            self.spotify_id = kwargs['spotify_id']
            del kwargs['spotify_id']
        if 'spotify_type' in kwargs.keys():
            self.spotify_type = kwargs['spotify_type']
            del kwargs['spotify_type']

        super().__init__(**kwargs)

    def __str__(self) -> str:
        if self.spotify_type is None:
            return self.text

        return '{} - {} - {}'.format(
            self.spotify_type,
            self.spotify_id,
            self.text
        )
