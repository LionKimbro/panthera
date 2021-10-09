"""guisys.py  -- GUI system

select(win)  -- select a window
  "win"  -- the tkinter name ("tkname") for a toplevel (ex: ".settings")
"""

import tkinter as tk

from symbols import *
from listdict import cue as list_cue
from listdict import val, val1, val01, req, srt
from listdict import EQ, NEQ, GT, LT, GTE, LTE
from listdict import CONTAINS, NCONTAINS, WITHIN, NWITHIN

# import menubar  -- REATTACH LATER


# Global Variables

g = {NEXTID: 1,
     TCL: {REQUEST: None, RESULT: None},
     MAPPING: None}


def nextid():
    """Return NEXTID, auto-increment."""
    g[NEXTID] += 1
    return g[NEXTID]-1


# Constants -- Window Kind & Information

records = [
    {TYPE: KIND,
     KIND: SETTINGS,
     TITLE: "Panthera: Settings",
     TKNAME: ".settings",
     UNIQUE: True
    },
    {TYPE: KIND,
     KIND: TAGSEARCH,
     TITLE: "Panthera: Tag Search",
     TKNAME: ".tagsearch",
     UNIQUE: True
    },
    {TYPE: KIND,
     KIND: MAPSEARCH,
     TITLE: "Panthera: Map Search",
     TKNAME: ".mapsearch",
     UNIQUE: True
    },
    {TYPE: KIND,
     KIND: TAG,
     TITLE: "Panthera: Tag Editor",
     TKNAME: ".tag",
     UNIQUE: False
    },
    {TYPE: KIND,
     KIND: MAP,
     TITLE: "Panthera: Map Editor",
     TKNAME: ".map",
     UNIQUE: False
    }
]

def record_for_kind(kind):
    list_cue(records)
    req(TYPE=KIND, KIND=kind)
    return val1()

def kind_tkname(kind):
    return record_for_kind(kind)[TKNAME]


# Global Variables -- Running Tasks

tasks = []

CLOSETOP="CLOSETOP"  # TYPE:CLOSETOP -- instructs to close TOPLEVEL
TOPLEVEL="TOPLEVEL"  # TOPLEVEL -- contains the toplevel window to close

CALL="CALL"  # TYPE:CALL -- instructs to call a specific fn
FN="FN"  # the function to call

EXIT="EXIT"  # TYPE:EXIT -- instructs to exit the program entirely


# Context Construction

ERR="ERR"  # requesting error default

S = []

def set(k, v): S[-1][k] = v

def get(k, default=None):
    for D in reversed(S):
        if k in D:
            return D[k]
    if default == ERR:
        raise KeyError(k)
    else:
        return default

def push(**D): S.append(D)

def pop(): return S.pop()


# Context Construction Keys

NAME="NAME"  # suggested string toplevel's name (other than "top")
# IMPORTANT: this name should be [a-z]*, otherwise
#            you risk making a bad tcl identifier...
TITLE="TITLE"


# Global Root & Functions -- Tk Fundamental

root = tk.Tk()

call = root.tk.call  # receives a list of literal strings
createcommand = root.tk.createcommand  # literal key?
tkeval = root.tk.eval  # direct; handled as a single string by tk


# Functions -- primary interfaces: peek, poke, tclexec, & mkcmd

def peek(tkname):
    """Peek a value.
    
    For example, peek("w") -> ".settings" (or whatever)
    """
    return tkeval('set '+tkname)

def poke(tkname, s):
    """Poke a string value literally into tk.
    
    Note that when you use CALL, it doesn't perform $-substitutions.
    So I perform substitutions literally for the key, and then use that for the set call.
    """
    subst_key = tkeval('subst '+tkname)  # perform any substitutions in tkname
    call('set', subst_key, s)  # use call, because it will work literally


def tclexec(tcl_code):
    """Run tcl code"""
    g[TCL][REQUEST] = tcl_code
    g[TCL][RESULT] = tkeval(tcl_code)
    return g[TCL][RESULT]

def mkcmd(tkname, fn):
    """Bind a tk command to a function"""
    createcommand(tkname, fn)


# Functions -- Tk main loop control

def loop():
    """Setup complete; Run main loop."""
    root.mainloop()


def after_idle():
    """Call mainloop_tasks() RIGHT AWAY, don't fuss for 100ms"""
    cancel()
    tclexec("after idle mainloop_tasks")


def schedule():
    """Schedule mainloop task, 100 ms into the future."""
    tclexec("set afterhandle [after 100 mainloop_tasks]")


def cancel():
    """Cancel the next scheduled mainloop task."""
    tclexec("after cancel $afterhandle")
    tclexec("unset afterhandle")


def mainloop_tasks():
    while tasks:
        D = tasks.pop()
        if D[TYPE] == CLOSETOP:
            name = D[TOPLEVEL]
            cue(name)
            tclexec("destroy $win")
            if not toplevels():
                task_exit()
                after_idle()
        elif D[TYPE] == CALL:
            D[FN]()
        elif D[TYPE] == EXIT:
            root.destroy()
    schedule()  # schedule the next run


# Functions -- main entry & debug

def debug():
    cancel()
    breakpoint()
    schedule()


# Functions -- Setup routine


def setup():
    tclexec("wm withdraw .")  # close initial tk window
    tclexec("option add *tearOff 0")  # turn off tear-off menus
    mkcmd("wm_delete_window", wm_delete_window)
    mkcmd("mainloop_tasks", mainloop_tasks)
    schedule()  # start the main loop


# Focus & Cue-ing

def cue(tkname=None):
    """Set tk's $w to tkname or currently focused window."""
    if tkname is None:
        tkname = focused()
    poke("w", tkname)

def cur():
    return peek("w")

def top():
    """Returns the toplevel for $w."""
    return tclexec("winfo toplevel $w")

def name():
    """Returns the name of $w, alone, without parents"""
    return tclexec("winfo name $w")

def wtype():
    """Returns the "window type" of $w.
    
    Important notes:
    * "window type" is not a tk concept;
      rather, Tk refers to a window's "class";
      see "winfo class" for more on this context
    * "window type" is made up by me, and consists of a matching symbol;
      presently (2021-10-09), I support here the symbols ENTRY and TEXT
    * if a matching symbol is not found, returns the window class, per Tk
    * HOWEVER: you should not use the window class --
      instead, I want you to extend symbols.py with a symbol to correspond
      with the window class, and that will be known as the window's "type"
    * because type is already used and essential to Python,
      I call the window type "wtype"
    """
    x = tclexec("winfo class $w")
    if x == "TEntry":
        return ENTRY
    elif x == "Text":
        return TEXT
    else:
        return x

def children():
    """Return the path names of the children of $w, as a list"""
    return tclexec("winfo children $w").split()

def text_get():
    """Return text from the cue'd window."""
    wt = wtype()
    if wt == ENTRY:
        return tclexec("$w get")
    elif wt == TEXT:
        return tclexec("$w get 1.0 end")
    else:
        raise ValueError("$w type not recognized")

def text_set(s):
    """Set text into the cue'd window."""
    wt = wtype()
    if wt == ENTRY:
        poke("tmp", s)
        tclexec("$w delete 0 end")
        tclexec("$w insert 0 $tmp")
    elif wt == TEXT:
        poke("tmp", s)
        tclexec("$w delete 1.0 end")
        tclexec("$w insert 1.0 $tmp")
    else:
        raise ValueError("$w type not recognized")

def set_win():
    """Don't call this for new code.
    
    This is for compatability with older code.
    It sets $win to the toplevel for w.
    """
    tclexec("set win [winfo toplevel $w]")

def cuekind(kind):
    """Cue a unique top-level, by kind.
    
    Note that it must be UNIQUE, otherwise behavior is undefined.
    """
    rec = record_for_kind(kind)
    assert rec[UNIQUE]
    cue(rec[TKNAME])


def tkname_to_top(tkname):
    poke("tmp", tkname)
    return tclexec("winfo toplevel $tmp")

def focused():
    """Return tkname of current Tk focused window.
    
    WARNING: While debugging, if the toplevel is no longer focused,
             you're going to get an empty string back, which,
             technically speaking, is correct.
    """
    return tclexec("focus")


# Top-Level Management

def lift():
    """Raise the cue'd window to the top level."""
    tclexec("focus $win")
    tclexec("raise $win")

def title(ttl):
    """Reset the title of the cue'd window's toplevel."""
    poke("tmp", ttl)
    tclexec("wm title [winfo toplevel $w] $tmp")

def exists():
    """Return True if the cue'd window still exists."""
    return tclexec("winfo exists $w") == '1'

def toplevels():
    return tclexec("winfo children .").split()

def toplevel(kind):
    """Create a new top-level, and return its name.
    
    Do not call this, if a unique window of the kind already exists.
    That should be detected beforehand, by calling exists(kind).
    
    The kind of the window is used to locate information about the window.
    * Whether it is multiple (tag editing windows) or singular (the settings window).
    * What title to use for the window.
    * How to name the window.
    
    The final tkname of the window is poked into "w", and returned.
    """
    rec = record_for_kind(kind)  # TITLE, UNIQUE, TKNAME
    tkname = rec[TKNAME]
    if not rec[UNIQUE]:
        tkname += str(nextid())
    cue(tkname)
    tclexec("toplevel $w")
    title(rec[TITLE])
    # menubar.attach()  -- REATTACH LATER
    tclexec("wm protocol $w WM_DELETE_WINDOW wm_delete_window")
    return tkname

def wm_delete_window():
    """A top-level is being closed.  Is the program over?"""
    cue(); task_closetop(top())


# Task Creation

def task_closetop(toplevel):
    tasks.append({TYPE:CLOSETOP,
                  TOPLEVEL: toplevel})

def task_fn(fn):
    tasks.append({TYPE:CALL,
                  FN: fn})

def task_exit():
    tasks.append({TYPE:EXIT})


