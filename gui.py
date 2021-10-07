"""guisys.py  -- GUI system

select(win)  -- select a window
  "win"  -- the tkinter name ("tkname") for a toplevel (ex: ".settings")
"""

import tkinter as tk


# Global Variables

NEXTID="NEXTID"

g = {NEXTID: 1}


def nextid():
    """Return NEXTID, auto-increment."""
    g[NEXTID] += 1
    return g[NEXTID]-1


# Global Variables -- TopLevel Tracking

open_toplevels = []  # list of toplevel identifiers


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

TITLE="TITLE"


# Basics

root = tk.Tk()

def poke(tkname, val):
    root.tk.call('set', tkname, val)

def peek(tkname):
    return root.tk.call('set', tkname)

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
    return root.tk.eval(tcl_code)


def loop():
    """Setup complete; Run main loop."""
    root.mainloop()


def setup():
    tclexec("wm withdraw .")  # close initial tk window
    tclexec("option add *tearOff 0")  # turn off tear-off menus
    mkcmd("wm_delete_window", wm_delete_window)
    mkcmd("mainloop_tasks", mainloop_tasks)
    tclexec("after 100 mainloop_tasks")


# Focus

tkname_to_toplevel = lambda s: "." + s.split(".")[1]

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

def toplevel():
    """Create a new top-level, and return its name.
    
    Also, pokes the name into "win," so it's ready to use.
    """
    name = ".top" + str(nextid())
    cue(name)
    tclexec("toplevel $win")
    ttl = get(TITLE)
    if ttl:
        poke("tmp", ttl)
        tclexec("wm title $win $tmp")
    tclexec("focus $win")  # focus the top-level
    open_toplevels.append(name)  # register the top-level
    tclexec("wm protocol $win WM_DELETE_WINDOW wm_delete_window")
    return name

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

def mainloop_tasks():
    while tasks:
        D = tasks.pop()
        if D[TYPE] == TYPE_CLOSETOP:
            name = D[TOPLEVEL]
            open_toplevels.remove(name)
            cue(name)
            tclexec("destroy $win")
        elif D[TYPE] == TYPE_CALL:
            D[FN]()
        elif D[TYPE] == TYPE_EXIT:
            root.destroy()
    if not open_toplevels:
        task_exit()
        after_idle()
    tclexec("after 100 mainloop_tasks")

