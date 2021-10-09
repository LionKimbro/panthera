"""winmap.py  -- a mapping between a window and a Python data structure

The mapping format is as follows:

    [("tk-window-path", (path, to, follow, into, D)),
      ...]
    
"tk-window-path" means the full path of a tk window.
    
The path to follow into D is per util.py's "path_set" and "path_get"
functions.


Use this in two steps:

  1. winmap.configure(D, mapping)

  2. winmap.store_to_window()
       or
     winmap.window_to_store()
"""

import gui
from gui import cue, text_set, text_get

import util
from util import path_set, path_get


def window_to_store(D, mapping):
    """load window paths into dictionary, according to configuration"""
    for (w, p) in mapping:
        cue(w)
        path_set(D, p, text_get())

def store_to_window(D, mapping):
    """load dictionary into window paths, according to configuration"""
    for (w, p) in mapping:
        cue(w)
        text_set(path_get(D, p))

