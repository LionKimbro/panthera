"""guisys.py  -- GUI system

select(win)  -- select a window
  "win"  -- the tkinter name ("tkname") for a toplevel (ex: ".settings")
"""

import tkinter as tk


# Basics

root = tk.Tk()

def strvar(tkname):
    """Return a tk.StringVar"""
    return tk.StringVar(name=tkname)


def mkcmd(tkname, fn):
    """Bind a tk command to a function"""
    root.tk.createcommand(tkname, fn)


def run(tcl_code):
    """Run tcl code"""
    return root.tk.eval(tcl_code)


def loop():
    """Setup complete; Run main loop."""
    root.mainloop()


def exit():
    root.destroy()


# Convenience

def focused():
    """Return tkname of current Tk focused widget"""
    return run("focus")




