#!/usr/bin/env python
from kivy import Config

from spdown.gui.app import SPDown

if __name__ == "__main__":
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.set('graphics', 'width', 960)
    Config.set('graphics', 'height', 565)

    SPDown().run()
