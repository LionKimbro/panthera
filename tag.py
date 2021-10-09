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

import gui
import settings
import data


# Data Dictionary for tag records

TAG="TAG"
TAGS="TAGS"
MNEMONICS="MNEMONICS"
TITLE="TITLE"
HOOK="HOOK"
DESCRIPTION="DESCRIPTION"
IDENTIFIER="IDENTIFIER"
CREATOR="CREATOR"
CREATED="CREATED"


STRING="STRING"  # type:string
LIST_OF_STRING="LIST_OF_STRING"  # type: [string, string, ...]

tag_records_data_dictionary = [
    {"key": TAG,
     "type": STRING,
     "subtype": "word",
     "desc": "the formal tag, as a word, that this record describes"},
    {"key": TAGS,
     "type": LIST_OF_STRING,
     "subtype": "list of words",
     "desc": "the bona fida tags that can be used to find this tag"},
    {"key": MNEMONICS,
     "type": LIST_OF_STRING,
     "subtype": "list of words",
     "desc": "the mnemonic words that can be used to find this tag"},
    {"key": TITLE,
     "type": STRING,
     "subtype": "human readable title",
     "desc": "the title for the formal tag"},
    {"key": HOOK,
     "type": STRING,
     "subtype": "human readable phrase",
     "desc": "a phrase that calls out some importance of the formal tag"},
    {"key": DESCRIPTION,
     "type": STRING,
     "subtype": "lines of human readable text",
     "desc": "a description of the formal tag; any pertinent details about it as well"},
    {"key": IDENTIFIER,
     "type": STRING,
     "subtype": "identifier",
     "desc": "the formal identifier (uri:urn:... or tag:...) for the tag"},
    {"key": CREATOR,
     "type": STRING,
     "subtype": "identifier",
     "desc": "the formal identifier of the person who created this tag"},
    {"key": CREATED,
     "type": STRING,
     "subtype": "iso-8601 date",
     "desc": "the date on which this tag record was first created, by its creator"}
]


# "h" -- normally, I use "g" to refer to clobals,
#        but these aren't general globals -- these are a SPECIFIC
#        memory imprint to or from a tag window,
#        so I am going one letter past g, to "h",
#        to demark this specific global data
h = {TAG: None,  # use window_to_h() to imprint this from the live window
     TAGS: None,
     MNEMONICS: None,
     TITLE: None,
     HOOK: None,
     DESCRIPTION: None,
     IDENTIFIER: None,
     CREATOR: None,
     CREATED: None}


tcl_code = """
grid columnconfigure $win 0 -weight 1

ttk::frame $win.tag_frame
grid $win.tag_frame -row 0 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.tag_frame.lbl -text "Tag:"
grid $win.tag_frame.lbl -row 0 -column 0
ttk::entry $win.tag_frame.widget -textvariable $win.tag_var -width 30
set $win.tag_var ""
grid $win.tag_frame.widget -row 0 -column 1

ttk::frame $win.tags_frame
grid $win.tags_frame -row 1 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.tags_frame.lbl -text "Tags:"
grid $win.tags_frame.lbl -row 0 -column 0
ttk::entry $win.tags_frame.widget -textvariable $win.tags_var
set $win.tags_var ""
grid $win.tags_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $win.tags_frame 1 -weight 1

ttk::frame $win.mnemonics_frame
grid $win.mnemonics_frame -row 2 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.mnemonics_frame.lbl -text "Mnemonics:"
grid $win.mnemonics_frame.lbl -row 0 -column 0
ttk::entry $win.mnemonics_frame.widget -textvariable $win.mnemonics_var
set $win.mnemonics_var ""
grid $win.mnemonics_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $win.mnemonics_frame 1 -weight 1

ttk::frame $win.title_frame
grid $win.title_frame -row 3 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.title_frame.lbl -text "Title:"
grid $win.title_frame.lbl -row 0 -column 0
ttk::entry $win.title_frame.widget -textvariable $win.title_var -width 60
set $win.title_var ""
grid $win.title_frame.widget -row 0 -column 1

ttk::frame $win.hook_frame
grid $win.hook_frame -row 4 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.hook_frame.lbl -text "Hook:"
grid $win.hook_frame.lbl -row 0 -column 0
ttk::entry $win.hook_frame.widget -textvariable $win.hook_var -width 60
set $win.hook_var ""
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
ttk::entry $win.identifier_frame.widget -textvariable $win.identifier_var
set $win.identifier_var ""
grid $win.identifier_frame.widget -row 0 -column 1 -sticky ew
grid columnconfigure $win.identifier_frame 1 -weight 1
ttk::checkbutton $win.identifier_frame.check -variable $win.identifier_chk -onvalue 1
set $win.identifier_chk 1
grid $win.identifier_frame.check -row 0 -column 2

ttk::frame $win.creator_frame
grid $win.creator_frame -row 7 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.creator_frame.lbl -text "Creator:"
grid $win.creator_frame.lbl -row 0 -column 0
ttk::entry $win.creator_frame.widget -textvariable $win.creator_var -width 50
set $win.creator_var ""
grid $win.creator_frame.widget -row 0 -column 1

ttk::frame $win.created_frame
grid $win.created_frame -row 8 -column 0 -padx 10 -pady "5 0" -sticky nsew
ttk::label $win.created_frame.lbl -text "Created:"
grid $win.created_frame.lbl -row 0 -column 0
ttk::entry $win.created_frame.widget -textvariable $win.created_var -width 12
set $win.created_var ""
grid $win.created_frame.widget -row 0 -column 1

ttk::frame $win.buttons_frame
grid $win.buttons_frame -row 9 -column 0 -padx 10 -pady 5 -sticky nsew
ttk::button $win.buttons_frame.btn_save -text "Save Tag" -command tag_save
grid $win.buttons_frame.btn_save -row 0 -column 0

ttk::button $win.buttons_frame.btn_load -text "Load Tag" -command tag_load
grid $win.buttons_frame.btn_load -row 0 -column 1

focus $win.tag_frame.widget
"""


def setup():
    gui.mkcmd("tag_save", save)
    gui.mkcmd("tag_load", load)


def new():
    """Create a new tag window.
    
    After you call this, call either .populate_default(), or
    populate_from(tag).  BUT: do so via gui.task_fn(lambda:...) and
    via gui.after_idle(), because it takes some time for Tk to update
    its focus model..!
    """
    gui.toplevel(gui.KIND_TAG)
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

def load():
    tag = peek("tag_var")
    D = data.find_tag(tag)
    if D:
        data.record_to_tag(D)
        h_to_window()
    else:
        print("not found:", tag)


def peek(k):
    """Peek a value within the currently cue'd tag window.
    
    ASSUMPTION: current $win is a tag window
    """
    return gui.peek("$win."+k)

def poke(k, s):
    """Poke a value within the currently cue'd tag window.
    
    ASSUMPTION: current $win is a tag window
    """
    gui.poke("$win."+k, s)


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

def window_to_h():
    """Imprint the cue'd tag window's data to memory."""
    h[TAG] = peek("tag_var")
    h[TAGS] = peek("tags_var").split()
    h[MNEMONICS] = peek("mnemonics_var").split()
    h[TITLE] = peek("title_var")
    h[HOOK] = peek("hook_var")
    h[DESCRIPTION] = gui.tclexec("$win.description_frame.widget get 1.0 end")
    h[IDENTIFIER] = peek("identifier_var")
    h[CREATOR] = peek("creator_var")
    h[CREATED] = peek("created_var")

def h_to_window():
    """Set the cue'd window's data from memory."""
    poke("tag_var", h[TAG])
    poke("tags_var", " ".join(h[TAGS]))
    poke("mnemonics_var", " ".join(h[MNEMONICS]))
    poke("title_var", h[TITLE])
    poke("hook_var", h[HOOK])
    gui.poke("tmp", h[DESCRIPTION])  # gui.poke is absolute
    gui.tclexec("$win.description_frame.widget delete 1.0 end")
    gui.tclexec("$win.description_frame.widget insert end $tmp")
    poke("identifier_var", h[IDENTIFIER])
    poke("identifier_chk", 0)
    poke("creator_var", h[CREATOR])
    poke("created_var", h[CREATED])

