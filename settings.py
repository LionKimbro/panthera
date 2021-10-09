"""
Settings window:

- user's own tag,
- user's authority (e-mail addr or domain)
- prefix for default new tag identifiers
  ("%AUTH" for user's authority, "%YEAR" "%MONTH" or "%DAY%" for the current day's date,)

...and a help button next to each for hover-over explanations about each...

     0                  1
   +------------------+---------------------------------------
  0| User's Tag:      | [ttk::entry] -- (settings.utag)
   | $win.utaglbl     | $win.utag      
   +------------------+---------------------------------------
  1| $win.utagexplain (ttk::label)
   +------------------+---------------------------------------
  2| User's Authority:| [ttk::entry] -- (settings.uauth)
   | $win.uauthlbl    | $win.uauth
   +------------------+---------------------------------------
  3| $win.uauthexplain (ttk::label)
   +------------------+---------------------------------------
  4| New Tag Prefix:  | [ttk::entry] -- (settings.tagidform)
   | $win.prefixlbl   | $win.prefix
   +------------------+---------------------------------------
  5| $win.prefixexplain (ttk::label)
   +------------------+---------------------------------------
  6| [tk::text $win.explanation -height 3]
   |                  .
   +------------------+---------------------------------------

"""

import gui
import data
import tag


tcl_code = """
ttk::label $win.utaglbl -text "User's Identifier:"
grid $win.utaglbl -row 0 -column 0 -sticky e -padx "10 5" -pady "10 5"

ttk::entry $win.utag -textvariable settings.utag
grid $win.utag -row 0 -column 1 -sticky ew -padx "0 10" -pady "10 5"

ttk::label $win.utagexplain -text "This is the RFC 4151 Tag URI for the user, and it should begin with 'tag:'."
grid $win.utagexplain -row 1 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"

set settings.utag "tag:lionkimbro@gmail.com,2022:person:example"


ttk::label $win.uauthlbl -text "User's Authority:"
grid $win.uauthlbl -row 2 -column 0 -sticky e -padx "10 5" -pady 5

ttk::entry $win.uauth -textvariable settings.uauth
grid $win.uauth -row 2 -column 1 -sticky ew -padx "0 10" -pady 5

ttk::label $win.uauthexplain -text "This is either an e-mail address, or a domain name, that the user controls."
grid $win.uauthexplain -row 3 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"

set settings.uauth "your-email@example.com"


ttk::label $win.tagidformlbl -text "New Tag Identifier Form:"
grid $win.tagidformlbl -row 4 -column 0 -sticky e -padx "10 5" -pady 5

ttk::entry $win.tagidform -textvariable settings.tagidform
grid $win.tagidform -row 4 -column 1 -sticky ew -padx "0 10" -pady 5

ttk::label $win.tagidformexplain -text "The form of a user tag.  It should probably be: %AUTH,%DAY:tag:%TAG, but could also use %MONTH or %YEAR."
grid $win.tagidformexplain -row 5 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"

set settings.tagidform "tag:%AUTH,%DAY:tag:%TAG"


grid columnconfigure $win 0 -weight 0
grid columnconfigure $win 1 -weight 1
"""


UTAG="UTAG"
UAUTH="UAUTH"
TAGIDFORM="TAGIDFORM"
settings_keys = [UTAG, UAUTH, TAGIDFORM]

g = {}


def setup():
    g[UTAG] = gui.strvar("settings.utag")
    g[UAUTH] = gui.strvar("settings.uauth")
    g[TAGIDFORM] = gui.strvar("settings.tagidform")


def open():
    """Open the settings window."""
    gui.cuekind(gui.KIND_SETTINGS)
    if gui.exists():
        gui.lift()
    else:
        gui.toplevel(gui.KIND_SETTINGS)
        gui.tclexec(tcl_code)
        load_from_record()


# Saving and Loading the Settings Record

def load_from_record():
    """Load current SETTINGS record into settings GUI variables."""
    D = data.settings_record()
    for (k,v) in D.items():
        if k in settings_keys:
            g[k].set(v)

def save_to_record():
    """Save GUI variables into SETTINGS record."""
    D = data.settings_record()
    for k in settings_keys:
        D[k] = g[k].get()


# Information Requests from other modules

def user_identifier():
    return g[UTAG].get()

