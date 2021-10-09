"""
Tag window:

- tag
- tags
- mnemonics
- title
- hook
- description (larger text area)
- identifier + generating checkbox
- creator
- date created

- user's authority (e-mail addr or domain)
- prefix for default new tag identifiers
  ("%AUTH" for user's authority, "%YEAR" "%MONTH" or "%DAY%" for the current day's date,)

...and a help button next to each for hover-over explanations about each...
"""

import time

from symbols import *
import gui
import settings
import data


# "h" -- normally, I use "g" to refer to clobals,
#        but these aren't general globals -- these are a SPECIFIC
#        memory imprint to or from a tag window,
#        so I am going one letter past g, to "h",
#        to demark this specific global data
#
#        use window_to_h() to imprint from the live window,
#        and h_to_window() to restore to the live window
#
h = {TAG: None,  # STR, word -- the formal tag, as a word, that this record describes
     TAGS: None,  # STRLIST, words -- the bona fida tags to find the tag
     MNEMONICS: None,  # STRLIST, words -- mnemonic tags to find the tag
     TITLE: None,  # STR, title -- the title for the formal tag
     HOOK: None,  # STR, phrase -- a phrase recalling the importance of the tag
     DESCRIPTION: None,  # STR, text -- long description of the tag
     IDENTIFIER: None,  # STR, id -- globally unique id for the tag
     CREATOR: None,  # STR, id -- globally unique id for the tag
     CREATED: None}  # STR, iso-8601 date -- date the tag was created


tcl_code = """
grid columnconfigure $win 0 -weight 1

ttk::frame $win.tag_frame
grid $win.tag_frame -row 0 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.tag_frame.lbl -text "Tag:"
grid $win.tag_frame.lbl -row 0 -column 0
ttk::entry $win.tag_frame.widget -width 30
grid $win.tag_frame.widget -row 0 -column 1

ttk::frame $win.tags_frame
grid $win.tags_frame -row 1 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.tags_frame.lbl -text "Tags:"
grid $win.tags_frame.lbl -row 0 -column 0
ttk::entry $win.tags_frame.widget
grid $win.tags_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $win.tags_frame 1 -weight 1

ttk::frame $win.mnemonics_frame
grid $win.mnemonics_frame -row 2 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.mnemonics_frame.lbl -text "Mnemonics:"
grid $win.mnemonics_frame.lbl -row 0 -column 0
ttk::entry $win.mnemonics_frame.widget
grid $win.mnemonics_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $win.mnemonics_frame 1 -weight 1

ttk::frame $win.title_frame
grid $win.title_frame -row 3 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.title_frame.lbl -text "Title:"
grid $win.title_frame.lbl -row 0 -column 0
ttk::entry $win.title_frame.widget -width 60
grid $win.title_frame.widget -row 0 -column 1

ttk::frame $win.hook_frame
grid $win.hook_frame -row 4 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.hook_frame.lbl -text "Hook:"
grid $win.hook_frame.lbl -row 0 -column 0
ttk::entry $win.hook_frame.widget -width 60
grid $win.hook_frame.widget -row 0 -column 1

ttk::frame $win.description_frame
grid $win.description_frame -row 5 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.description_frame.lbl -text "Description:"
grid $win.description_frame.lbl -row 0 -column 0
tk::text $win.description_frame.widget -width 80 -height 3
grid $win.description_frame.widget -row 0 -column 1  -sticky ew
grid columnconfigure $win.description_frame 1 -weight 1

ttk::frame $win.identifier_frame
grid $win.identifier_frame -row 6 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.identifier_frame.lbl -text "Identifier:"
grid $win.identifier_frame.lbl -row 0 -column 0
ttk::entry $win.identifier_frame.widget
grid $win.identifier_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $win.identifier_frame 1 -weight 1
ttk::checkbutton $win.identifier_frame.check -onvalue 1
grid $win.identifier_frame.check -row 0 -column 2

ttk::frame $win.creator_frame
grid $win.creator_frame -row 7 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.creator_frame.lbl -text "Creator:"
grid $win.creator_frame.lbl -row 0 -column 0
ttk::entry $win.creator_frame.widget -width 50
grid $win.creator_frame.widget -row 0 -column 1

ttk::frame $win.created_frame
grid $win.created_frame -row 8 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.created_frame.lbl -text "Created:"
grid $win.created_frame.lbl -row 0 -column 0
ttk::entry $win.created_frame.widget -width 12
grid $win.created_frame.widget -row 0 -column 1

ttk::frame $win.buttons_frame
grid $win.buttons_frame -row 9 -column 0 -padx 10 -pady 5 -sticky nsew
ttk::button $win.buttons_frame.btn_save -text "Save Tag" -command tag_save
grid $win.buttons_frame.btn_save -row 0 -column 0

focus $win.tag_frame.widget
"""


def setup():
    gui.mkcmd("tag_save", save)


def new():
    """Create a new tag window.
    
    After you call this, call either .populate_default(), or
    populate_from(tag).  BUT: do so via gui.task_fn(lambda:...) and
    via gui.after_idle(), because it takes some time for Tk to update
    its focus model..!
    """
    gui.toplevel(TAG)
    gui.tclexec(tcl_code)
    gui.lift()

def populate_default():
    """Populate tag window with default data.

    ASSUMPTION: window cue'd
    """
    default_h()
    h_to_window()

def populate_from(tag):
    """Populate tag window from a tag in data, id'ed by name.
    
    ASSUMPTION: window cue'd
    
    If it worked, returns True.
    If no such tag found, does nothing and returns False.
    """
    D = data.find_tag(tag)
    if D:
        data.record_to_tag(D)
        h_to_window()
        return True
    else:
        return False


def save():
    window_to_h()
    data.add_tag()


# Functions -- global h data blank/default/keep/restore

def blank_h():
    """Blank the memory."""
    h[TAG] = ""
    h[TAGS] = []
    h[MNEMONICS] = []
    h[TITLE] = ""
    h[HOOK] = ""
    h[DESCRIPTION] = ""
    h[IDENTIFIER] = ""
    h[CREATOR] = ""
    h[CREATED] = ""

def default_h():
    h[TAG] = ""
    h[TAGS] = []
    h[MNEMONICS] = []
    h[TITLE] = ""
    h[HOOK] = ""
    h[DESCRIPTION] = ""
    h[IDENTIFIER] = ""
    h[CREATOR] = settings.user_identifier()
    h[CREATED] = time.strftime("%Y-%m-%d")


mapping = [
    (TAG, "$win.tag_frame.widget"),
    (TAGS, "$win.tags_frame.widget"),
    (MNEMONICS, "$win.mnemonics_frame.widget"),
    (TITLE, "$win.title_frame.widget"),
    (HOOK, "$win.hook_frame.widget"),
    (IDENTIFIER, "$win.identifier_frame.widget"),
    (CREATOR, "$win.creator_frame.widget"),
    (CREATED, "$win.created_frame.widget")
]

def window_to_h():
    """Imprint the cue'd tag window's data to memory."""
    for (hvar, widget) in mapping:
        h[hvar] = read(widget)
    h[DESCRIPTION] = gui.tclexec("$win.description_frame.widget get 1.0 end")

def h_to_window():
    """Set the cue'd window's data from memory."""
    for (hvar, widget) in mapping:
        write(widget, h[hvar])
    gui.poke("tmp", h[DESCRIPTION])  # gui.poke is absolute
    gui.tclexec("$win.description_frame.widget delete 1.0 end")
    gui.tclexec("$win.description_frame.widget insert end $tmp")

