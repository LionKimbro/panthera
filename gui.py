"""guisys.py  -- GUI system

select(win)  -- select a window
  "win"  -- the tkinter name ("tkname") for a toplevel (ex: ".settings")
"""

import tkinter as tk

from listdict import cue as list_cue
from listdict import val, val1, val01, req, srt
from listdict import EQ, NEQ, GT, LT, GTE, LTE
from listdict import CONTAINS, NCONTAINS, WITHIN, NWITHIN

import menubar


# Global Variables

NEXTID="NEXTID"
REQUEST_TCLEXEC="REQUEST_TCLEXEC"  # for debug reasons; last tclexec request
RESULT_TCLEXEC="RESULT_TCLEXEC"  # for debug reasons; tclexec last result
LOOP_HANDLE="LOOP_HANDLE"  # handle of next scheduled call to mainloop_tasks

g = {NEXTID: 1,
     REQUEST_TCLEXEC: None,
     RESULT_TCLEXEC: None,
     LOOP_HANDLE: None}


def nextid():
    """Return NEXTID, auto-increment."""
    g[NEXTID] += 1
    return g[NEXTID]-1


# Constants -- Window Kind & Information

TYPE="TYPE"; TYPE_KIND="TYPE_KIND"
KIND="KIND"
KIND_SETTINGS="KIND_SETTINGS"
KIND_TAGSEARCH="KIND_TAGSEARCH"
KIND_MAPSEARCH="KIND_MAPSEARCH"
KIND_TAG="KIND_TAG"
KIND_MAP="KIND_MAP"
TITLE="TITLE"  # title to use
TKNAME="TKNAME"  # tkname string, or, tkname prefix; string, and starts with a period
UNIQUE="UNIQUE"  # True/False -- is this window unique?

records = [
    {TYPE: TYPE_KIND,
     KIND: KIND_SETTINGS,
     TITLE: "Panthera: Settings",
     TKNAME: ".settings",
     UNIQUE: True
    },
    {TYPE: TYPE_KIND,
     KIND: KIND_TAGSEARCH,
     TITLE: "Panthera: Tag Search",
     TKNAME: ".tagsearch",
     UNIQUE: True
    },
    {TYPE: TYPE_KIND,
     KIND: KIND_MAPSEARCH,
     TITLE: "Panthera: Map Search",
     TKNAME: ".mapsearch",
     UNIQUE: True
    },
    {TYPE: TYPE_KIND,
     KIND: KIND_TAG,
     TITLE: "Panthera: Tag Editor",
     TKNAME: ".tag",
     UNIQUE: False
    },
    {TYPE: TYPE_KIND,
     KIND: KIND_MAP,
     TITLE: "Panthera: Map Editor",
     TKNAME: ".map",
     UNIQUE: False
    }
]

def record_for_kind(kind):
    list_cue(records)
    req(TYPE=TYPE_KIND, KIND=kind)
    return val1()

def kind_tkname(kind):
    return record_for_kind(kind)[TKNAME]


# Global Variables -- Running Tasks

tasks = []

TYPE="TYPE"  # task type to run

TYPE_CLOSETOP="CLOSETOP"  # TYPE:CLOSETOP -- instructs to close TOPLEVEL
TOPLEVEL="TOPLEVEL"  # TOPLEVEL -- contains the toplevel window to close

TYPE_CALL="CALL"  # TYPE:CALL -- instructs to call a specific fn
FN="FN"  # the function to call

TYPE_EXIT="EXIT"  # TYPE:EXIT -- instructs to exit the program entirely


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


# Basics

root = tk.Tk()

def poke(tkname, val):
    """Poke a value literally into tk.
    
    Note that when you use CALL, it doesn't perform $-substitutions.
    So I call peek first, to evaluate the tkname, and then use that for the set call.
    """
    tclexec('set poketmp '+tkname)  # directly perform substitutions into poketmp
    tmp = tclexec('set poketmp')
    root.tk.call('set', tmp, val)

def peek(tkname):
    tclexec('set poketmp '+tkname)  # directly perform substitutions into poketmp
    tmp = tclexec('set poketmp')
    return root.tk.call('set', tmp)

def strvar(tkname):
    """Return a tk.StringVar"""
    return tk.StringVar(name=tkname)


def mkcmd(tkname, fn):
    """Bind a tk command to a function"""
    root.tk.createcommand(tkname, fn)


def after_idle():
    """Call mainloop_tasks() RIGHT AWAY, don't wait 100ms"""
    tclexec("after idle mainloop_tasks")


def tclexec(tcl_code):
    """Run tcl code"""
    g[REQUEST_TCLEXEC] = tcl_code
    g[RESULT_TCLEXEC] = root.tk.eval(tcl_code)
    return g[RESULT_TCLEXEC]


def loop():
    """Setup complete; Run main loop."""
    root.mainloop()


def setup():
    tclexec("wm withdraw .")  # close initial tk window
    tclexec("option add *tearOff 0")  # turn off tear-off menus
    mkcmd("wm_delete_window", wm_delete_window)
    mkcmd("mainloop_tasks", mainloop_tasks)
    schedule()  # start the main loop


# Focus

def tkname_to_toplevel(s):
    poke("tmp", s)
    return tclexec("winfo toplevel $tmp")

def focused():
    """Return tkname of current Tk focused widget.
    
    WARNING: While debugging, if the window is no longer focused,
             you're going to get an empty string back, which,
             technically speaking, is correct.
    """
    return tclexec("focus")

def focused_toplevel():
    """Return tkname of current focused toplevel widget.
    
    WARNING: While debugging, if the window is no longer focused,
             you're going to get an empty string back, which,
             technically speaking, is correct.
    """
    return tkname_to_toplevel(focused())


# Top-Level Management

def cue(tkname=None):
    """Cue a top-level for use.
    
    If tkname is None, uses the currently focused top-level window.
    """
    if tkname is None:
        tkname = focused_toplevel()
    poke("win", tkname)

def cuekind(kind):
    """Cue a unique top-level, by kind.
    
    Note that it must be UNIQUE, otherwise behavior is undefined.
    """
    rec = record_for_kind(kind)
    assert rec[UNIQUE]
    cue(rec[TKNAME])

def lift():
    """Raise the cue'd window to the top level."""
    tclexec("focus $win")
    tclexec("raise $win")

def title(ttl):
    """Entitle cue'd window."""
    poke("tmp", ttl)
    tclexec("wm title $win $tmp")

def exists():
    """Return True if the cue'd window still exists."""
    return tclexec("winfo exists $win") == '1'

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
    
    The final tkname of the window is poked into "win", and returned.
    """
    rec = record_for_kind(kind)  # TITLE, UNIQUE, TKNAME
    tkname = rec[TKNAME]
    if not rec[UNIQUE]:
        tkname += str(nextid())
    cue(tkname)
    tclexec("toplevel $win")
    title(rec[TITLE])
    menubar.attach()
    tclexec("wm protocol $win WM_DELETE_WINDOW wm_delete_window")
    return tkname

def wm_delete_window():
    """A top-level is being closed.  Is the program over?"""
    task_closetop(focused_toplevel())


# Task Creation

def task_closetop(toplevel):
    tasks.append({TYPE:TYPE_CLOSETOP,
                  TOPLEVEL: toplevel})

def task_fn(fn):
    tasks.append({TYPE:TYPE_CALL,
                  FN: fn})

def task_exit():
    tasks.append({TYPE:TYPE_EXIT})


# Main Loop Checks

def schedule():
    """Schedule mainloop task, 100 ms into the future."""
    g[LOOP_HANDLE] = tclexec("after 100 mainloop_tasks")

def cancel():
    """Cancel the next scheduled mainloop task."""
    poke("tmp", g[LOOP_HANDLE])
    tclexec("after cancel $tmp")
    g[LOOP_HANDLE] = None

def mainloop_tasks():
    while tasks:
        D = tasks.pop()
        if D[TYPE] == TYPE_CLOSETOP:
            name = D[TOPLEVEL]
            cue(name)
            tclexec("destroy $win")
            if not toplevels():
                task_exit()
                after_idle()
        elif D[TYPE] == TYPE_CALL:
            D[FN]()
        elif D[TYPE] == TYPE_EXIT:
            root.destroy()
    schedule()  # schedule the next run

def pause():
    """Toggle mainloop execution routine."""
    
    
def debug():
    cancel()
    breakpoint()
    schedule()

