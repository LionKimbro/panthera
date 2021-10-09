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


0   0 [ .cont.lbl     [ .cont.widget.................] [.cont.button                          ] $win.cont

0   1 [ .with.lbl  : [ .with.widget................................] [.with.button            ] $win.with

1   2 [ .results.lbl        w:0                                                               ] $win.results

      [ .results.list....................................................].results.s
      [ [................................................................][@] ]
      [ [...................w:1........................................   w:0   
      [ [................................................................][@] ]
      [ [................................................................][|] ]
      [ [................................................................][|] ]
      [ [................................................................][v] ]


"""

import time

import gui
import settings
import data
import tag


tcl_code = """
grid columnconfigure $win 0 -weight 1
grid rowconfigure $win 2 -weight 1

ttk::frame $win.cont
grid $win.cont -row 0 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.cont.lbl -text "Tag Contains:"
grid $win.cont.lbl -row 0 -column 0
ttk::entry $win.cont.widget -textvariable tagsearch.contains_var -width 30
set tagsearch.contains_var ""
grid $win.cont.widget -row 0 -column 1
ttk::button $win.cont.button -text "Search" -command tagsearch_contains
grid $win.cont.button -row 0 -column 2


ttk::frame $win.with
grid $win.with -row 1 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.with.lbl -text "Tagged With:"
grid $win.with.lbl -row 0 -column 0
ttk::entry $win.with.widget -textvariable tagsearch.with_var -width 60
set tagsearch.with_var ""
grid $win.with.widget -row 0 -column 1
ttk::button $win.with.button -text "Search" -command tagsearch_with
grid $win.with.button -row 0 -column 2


ttk::frame $win.results
grid $win.results -row 2 -column 0 -padx 10 -pady "5 10" -sticky nsew
grid rowconfigure $win.results 1 -weight 1
grid columnconfigure $win.results 0 -weight 1

ttk::label $win.results.lbl -text "Results:"
grid $win.results.lbl -row 0 -column 0 -sticky nswe
tk::listbox $win.results.widget -height 6 -selectmode browse
grid $win.results.widget -row 1 -column 0 -sticky nsew
ttk::scrollbar $win.results.s -orient vertical -command "$win.results.widget yview"
grid $win.results.s -row 1 -column 1 -sticky nsew

bind $win.results.widget <Double-1> tagsearch_open

focus $win.cont.widget
"""

# /!\ TODO!!!  SCROLLBAR HOOKUP IS INCOMPLETE..!


# Global Variables

CONTAINS="CONTAINS"
WITH="WITH"

g = {CONTAINS: None, WITH: None}


# Functions

def setup():
    g[CONTAINS] = gui.strvar("tagsearch.contains_var")
    g[WITH] = gui.strvar("tagsearch.with_var")
    gui.mkcmd("tagsearch_contains", tagsearch_contains)
    gui.mkcmd("tagsearch_with", tagsearch_with)
    gui.mkcmd("tagsearch_open", tagsearch_open)


def open():
    """Open the tag search window."""
    gui.cuekind(TAGSEARCH)
    if gui.exists():
        gui.lift()
    else:
        gui.toplevel(TAGSEARCH)
        gui.tclexec(tcl_code)


def clear():
    gui.tclexec("$win.results.widget delete 0 end")

def add(tag):
    gui.poke("tmp", tag)
    gui.tclexec("$win.results.widget insert end $tmp")

def listtags(tag_records):
    clear()
    for rec in tag_records:
        add(rec["TAG"])

def selected():
    return gui.tclexec("$win.results.widget get [$win.results.widget curselection]")


# Functions -- callbacks

def tagsearch_contains():
    gui.cue()
    listtags(data.list_tags_containing(g[CONTAINS].get()))

def tagsearch_with():
    gui.cue()
    listtags(data.list_tags_tagged(g[WITH].get()))

def tagsearch_open():
    gui.cue()
    tagname = selected()
    tag.new()
    tag.populate_from(tagname)

