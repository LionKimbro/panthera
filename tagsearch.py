"""tagsearch.py -- a window for searching for tags

Tag Search window:

w row
- ---
0   0 [ Tag Contains: [..tagsearch.contains_var......] [Search] ] -command tagsearch_contains

0   1 [ Tagged With: [...tagsearch.with_var........................] [Search] ]  -command tagsearch_with

0   2 [ Results ]

1   3 [ [................................................................][^] ]
      [ [................................................................][@] ]
      [ [................................................................][@] ]
      [ [................................................................][@] ]
      [ [................................................................][|] ]
      [ [................................................................][|] ]
      [ [................................................................][v] ]


0   0 [ .cont.lbl     [ .cont.widget.................] [.cont.button                          ] .tagsearch.cont

0   1 [ .with.lbl  : [ .with.widget................................] [.with.button            ] .tagsearch.with

1   2 [ .results.lbl        w:0                                                               ] .tagsearch.results

      [ .results.list....................................................].results.s
      [ [................................................................][@] ]
      [ [...................w:1........................................   w:0   
      [ [................................................................][@] ]
      [ [................................................................][|] ]
      [ [................................................................][|] ]
      [ [................................................................][v] ]


"""

import time

from symbols import *

import gui
import winmap
import tag
import tagrecords
import listdict


tcl_code = """
grid columnconfigure .tagsearch 0 -weight 1
grid rowconfigure .tagsearch 2 -weight 1

ttk::frame .tagsearch.cont
grid .tagsearch.cont -row 0 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label .tagsearch.cont.lbl -text "Tag Contains:"
grid .tagsearch.cont.lbl -row 0 -column 0
ttk::entry .tagsearch.cont.widget -width 30
grid .tagsearch.cont.widget -row 0 -column 1
ttk::button .tagsearch.cont.button -text "Search" -command tagsearch_contains
grid .tagsearch.cont.button -row 0 -column 2


ttk::frame .tagsearch.with
grid .tagsearch.with -row 1 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label .tagsearch.with.lbl -text "Tagged With:"
grid .tagsearch.with.lbl -row 0 -column 0
ttk::entry .tagsearch.with.widget -width 60
grid .tagsearch.with.widget -row 0 -column 1
ttk::button .tagsearch.with.button -text "Search" -command tagsearch_with
grid .tagsearch.with.button -row 0 -column 2


ttk::frame .tagsearch.results
grid .tagsearch.results -row 2 -column 0 -padx 10 -pady "5 10" -sticky nsew
grid rowconfigure .tagsearch.results 1 -weight 1
grid columnconfigure .tagsearch.results 0 -weight 1

ttk::label .tagsearch.results.lbl -text "Results:"
grid .tagsearch.results.lbl -row 0 -column 0 -sticky nswe
tk::listbox .tagsearch.results.widget -height 6 -selectmode browse
grid .tagsearch.results.widget -row 1 -column 0 -sticky nsew
ttk::scrollbar .tagsearch.results.s -orient vertical -command ".tagsearch.results.widget yview"
grid .tagsearch.results.s -row 1 -column 1 -sticky nsew

bind .tagsearch.results.widget <Double-1> tagsearch_open

focus .tagsearch.cont.widget
"""

# /!\ TODO!!!  SCROLLBAR HOOKUP IS INCOMPLETE..!


# Functions

def setup():
    gui.mkcmd("tagsearch_contains", tagsearch_contains)
    gui.mkcmd("tagsearch_with", tagsearch_with)
    gui.mkcmd("tagsearch_open", tagsearch_open)


mapping = [(".tagsearch.cont.widget", CONTAINS, STR),
           (".tagsearch.with.widget", WITH, STRLIST)]

def values():
    D = {}
    winmap.window_to_store(D, mapping)
    return D


def open():
    """Open the tag search window."""
    if gui.toplevel_unique(".tagsearch", "Panthera: Tag Search"):
        gui.tclexec(tcl_code)


def cue_listbox():
    gui.cue(".tagsearch.results.widget")

def clear():
    gui.tclexec(".tagsearch.results.widget delete 0 end")

def add(tag):
    gui.poke("tmp", tag)
    gui.tclexec(".tagsearch.results.widget insert end $tmp")

def listtags(tag_records):
    clear()
    for rec in tag_records:
        add(rec["TAG"])


# Functions -- callbacks

def tagsearch_contains():
    substr = values()[CONTAINS]
    tagrecords.list_tags_containing(substr)
    L = listdict.map(TAG)
    cue_listbox()
    gui.list_set(L)

def tagsearch_with():
    tags = values()[WITH]
    tagrecords.list_tags_tagged(tags)
    L = listdict.map(TAG)
    cue_listbox()
    gui.list_set(L)

def tagsearch_open():
    cue_listbox()
    tagname = gui.list_selected()
    tag.make(tagname)

