"""tag.py  -- panthera tag window

See tagrecords.py for the structure of a tag record.
"""

import time

from symbols import *

import gui
import winmap
import tagrecords


tcl_code = """
grid columnconfigure $top 0 -weight 1

ttk::frame $top.tag_frame
grid $top.tag_frame -row 0 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.tag_frame.lbl -text "Tag:"
grid $top.tag_frame.lbl -row 0 -column 0
ttk::entry $top.tag_frame.widget -width 30
grid $top.tag_frame.widget -row 0 -column 1

ttk::frame $top.tags_frame
grid $top.tags_frame -row 1 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.tags_frame.lbl -text "Tags:"
grid $top.tags_frame.lbl -row 0 -column 0
ttk::entry $top.tags_frame.widget
grid $top.tags_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $top.tags_frame 1 -weight 1

ttk::frame $top.mnemonics_frame
grid $top.mnemonics_frame -row 2 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.mnemonics_frame.lbl -text "Mnemonics:"
grid $top.mnemonics_frame.lbl -row 0 -column 0
ttk::entry $top.mnemonics_frame.widget
grid $top.mnemonics_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $top.mnemonics_frame 1 -weight 1

ttk::frame $top.title_frame
grid $top.title_frame -row 3 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.title_frame.lbl -text "Title:"
grid $top.title_frame.lbl -row 0 -column 0
ttk::entry $top.title_frame.widget -width 60
grid $top.title_frame.widget -row 0 -column 1

ttk::frame $top.hook_frame
grid $top.hook_frame -row 4 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.hook_frame.lbl -text "Hook:"
grid $top.hook_frame.lbl -row 0 -column 0
ttk::entry $top.hook_frame.widget -width 60
grid $top.hook_frame.widget -row 0 -column 1

ttk::frame $top.description_frame
grid $top.description_frame -row 5 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.description_frame.lbl -text "Description:"
grid $top.description_frame.lbl -row 0 -column 0
tk::text $top.description_frame.widget -width 80 -height 3
grid $top.description_frame.widget -row 0 -column 1  -sticky ew
grid columnconfigure $top.description_frame 1 -weight 1

ttk::frame $top.identifier_frame
grid $top.identifier_frame -row 6 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.identifier_frame.lbl -text "Identifier:"
grid $top.identifier_frame.lbl -row 0 -column 0
ttk::entry $top.identifier_frame.widget
grid $top.identifier_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $top.identifier_frame 1 -weight 1
ttk::button $top.identifier_frame.assign -text "Build Identifier" -command tag_buildid
grid $top.identifier_frame.assign -row 0 -column 2

ttk::frame $top.creator_frame
grid $top.creator_frame -row 7 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.creator_frame.lbl -text "Creator:"
grid $top.creator_frame.lbl -row 0 -column 0
ttk::entry $top.creator_frame.widget -width 50
grid $top.creator_frame.widget -row 0 -column 1

ttk::frame $top.created_frame
grid $top.created_frame -row 8 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $top.created_frame.lbl -text "Created:"
grid $top.created_frame.lbl -row 0 -column 0
ttk::entry $top.created_frame.widget -width 12
grid $top.created_frame.widget -row 0 -column 1

ttk::frame $top.buttons_frame
grid $top.buttons_frame -row 9 -column 0 -padx 10 -pady 5 -sticky nsew
ttk::button $top.buttons_frame.btn_save -text "Save Tag" -command tag_save
grid $top.buttons_frame.btn_save -row 0 -column 0

focus $top.tag_frame.widget
"""


def setup():
    """initializing the module"""
    gui.mkcmd("tag_save", save)
    gui.mkcmd("tag_buildid", buildid)


# Functions -- creating a new window

def construct():
    """Construct the frame of a new tag window.
    
    This is only to be called by either new(), or make(tag).
    """
    gui.toplevel_recurring(".tag")
    gui.tclexec(tcl_code)

def new():
    """Create a tag window, that is blank, ready to be filled out."""
    construct()
    gui.cue_top()
    gui.title("Panthera: New Tag")
    rec_to_window(tagrecords.default())

def make(tag):
    """Create a tag window, representing the given pre-existing tag."""
    construct()
    gui.cue_top()
    gui.title("Panthera: Tag: "+tag)
    rec_to_window(tagrecords.find(tag))
    gui.cue("$top.tag_frame.widget")
    gui.text_ro()


# Functions -- Callbacks

def save():
    gui.cue()
    gui.cue_top()
    tagrecords.add(window_to_rec())

def buildid():
    import settings
    gui.cue()
    gui.cue_top()
    rec = window_to_rec()
    gui.cue("$top.identifier_frame.widget")
    gui.text_set(settings.make_tag_identifier(rec[TAG]))


# Functions -- record to window, and vice versa

mapping = [
    ("$top.tag_frame.widget", TAG, STR),
    ("$top.tags_frame.widget", TAGS, STRLIST),
    ("$top.mnemonics_frame.widget", MNEMONICS, STRLIST),
    ("$top.title_frame.widget", TITLE, STR),
    ("$top.hook_frame.widget", HOOK, STR),
    ("$top.identifier_frame.widget", IDENTIFIER, STR),
    ("$top.creator_frame.widget", CREATOR, STR),
    ("$top.created_frame.widget", CREATED, STR)
]

def window_to_rec():
    D = {}
    winmap.window_to_store(D, mapping)
    return D

def rec_to_window(D):
    winmap.store_to_window(D, mapping)

