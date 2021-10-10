"""winmap.py  -- a mapping between a window and a Python data structure

The mapping format is as follows:

    [("tk-window-path", key, type),
      ...]
    
"tk-window-path" means the full path of a tk window;
  VERY IMPORTANTLY, it may contain substitutions.

"k" is a path into a dictionary.

"type" is either STR or TAGS
  STR: a literally string, passed through directly
  STRLIST: a list of strings, split on newlines
    Tk widget <-- " ".join(L)   s.split() --> Python value
"""

from symbols import *

import gui


def window_to_store(D, mapping):
    """load window paths into dictionary, according to configuration"""
    for (w, k, t) in mapping:
        gui.cue(w)
        val = gui.text_get()
        if t == STR:
            D[k] = val
        elif t == STRLIST:
            D[k] = val.split()
        else:
            raise ValueError

def store_to_window(D, mapping):
    """load dictionary into window paths, according to configuration"""
    for (w, k, t) in mapping:
        gui.cue(w)
        if t == STR:
            gui.text_set(D[k])
        elif t == STRLIST:
            gui.text_set(" ".join(D[k]))
        else:
            raise ValueError

