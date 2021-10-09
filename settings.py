"""
Settings window:

- user's own tag,
- user's authority (e-mail addr or domain)
- prefix for default new tag identifiers
  ("%AUTH" for user's authority, "%YEAR" "%MONTH" or "%DAY%" for the current day's date,)

...and a help button next to each for hover-over explanations about each...
"""

import time

from symbols import *

import gui
import winmap
#import data


tcl_code = """
ttk::label .settings.userid_lbl -text "User's Identifier:"
grid .settings.userid_lbl -row 0 -column 0 -sticky e -padx "10 5" -pady "10 5"

ttk::entry .settings.userid
grid .settings.userid -row 0 -column 1 -sticky ew -padx "0 10" -pady "10 5"

ttk::label .settings.useridexplain -text "This is the RFC 4151 Tag URI for the user, and it should begin with 'tag:'."
grid .settings.useridexplain -row 1 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"


ttk::label .settings.uauth_lbl -text "User's Authority:"
grid .settings.uauth_lbl -row 2 -column 0 -sticky e -padx "10 5" -pady 5

ttk::entry .settings.uauth
grid .settings.uauth -row 2 -column 1 -sticky ew -padx "0 10" -pady 5

ttk::label .settings.uauthexplain -text "This is either an e-mail address, or a domain name, that the user controls."
grid .settings.uauthexplain -row 3 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"


ttk::label .settings.tagidformlbl -text "New Tag Identifier Form:"
grid .settings.tagidformlbl -row 4 -column 0 -sticky e -padx "10 5" -pady 5

ttk::entry .settings.tagidform
grid .settings.tagidform -row 4 -column 1 -sticky ew -padx "0 10" -pady 5

ttk::label .settings.tagidformexplain -text "The form of a user tag.  It should probably be: %AUTH,%DAY:tag:%TAG, but could also use %MONTH or %YEAR."
grid .settings.tagidformexplain -row 5 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"


grid columnconfigure .settings 0 -weight 0
grid columnconfigure .settings 1 -weight 1
"""


g = {USER:
     {IDENTIFIER: "",  # STR, id -- the user's globally unique identifier
      AUTHORITY: ""},  # STR, e-mail or domain -- the user's authority claim
     PATTERN: ""}  # STR, special -- pattern to apply for new tags

g[USER][IDENTIFIER] = "tag:example.com,2022:person:your-name-here"
g[USER][AUTHORITY] = "your-email-here@gmail.com"
g[PATTERN] = "tag:%AUTH,%DAY:tag:%TAG"


def open():
    """Open the settings window."""
    gui.cuekind(SETTINGS)
    if gui.exists():
        gui.lift()
    else:
        gui.toplevel(SETTINGS)
        gui.tclexec(tcl_code)
        # load_from_record()


mapping = [
    (".settings.userid", (USER, IDENTIFIER)),
    (".settings.uauth", (USER, AUTHORITY)),
    (".settings.tagidform", (PATTERN,))
]

# Functions -- Window <-> g

def window_to_g():
    """Store window contents to g-vars."""
    winmap.window_to_store(g, mapping)

def g_to_window():
    """Recover window contents from g-vars."""
    winmap.store_to_window(g, mapping)


# Saving and Loading

def load(data):
    """Called from data at load time, with data for this module."""
    g.update(data)

def save():
    """Called from data at save time; Supply with data to save."""
    return g


# Information Requests from other modules

def user_identifier():
    return g[USER][IDENTIFIER]

def make_tag_identifier(tag):
    s = g[TAG][PATTERN]
    s = s.replace("%TAG", tag)
    s = s.replace("%AUTH", g[USER][AUTHORITY])
    s = s.replace("%DAY", time.strftime("%Y-%m-%d"))
    s = s.replace("%MONTH", time.strftime("%Y-%m"))
    s = s.replace("%YEAR", time.strftime("%Y"))
    return s

