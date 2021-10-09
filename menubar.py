"""menubar.py  -- the standard menu bar for the Panthera windows"""


import data
import gui
import settings
import tagsearch
import tag


tcl_code = """
menu $win.mbar
$win configure -menu $win.mbar

menu $win.mbar.file
menu $win.mbar.new
menu $win.mbar.search
menu $win.mbar.help

$win.mbar add cascade -menu $win.mbar.file -label Panthera
$win.mbar add cascade -menu $win.mbar.new -label New
$win.mbar add cascade -menu $win.mbar.search -label Search
$win.mbar add cascade -menu $win.mbar.help -label Help

$win.mbar.file add command -label "Settings" -command settings
$win.mbar.file add separator
$win.mbar.file add command -label "Add Source"
$win.mbar.file add command -label "Save" -command save
$win.mbar.file add separator
$win.mbar.file add command -label "Exit" -command exit

$win.mbar.new add command -label "New Tag" -command newtag
$win.mbar.new add command -label "New Map"

$win.mbar.search add command -label "for Tag" -command tagsearch
$win.mbar.search add command -label "for Map"

$win.mbar.help add command -label "Tutorial"
$win.mbar.help add command -label "Contact"
$win.mbar.help add separator
$win.mbar.help add command -label "About"
$win.mbar.help add separator
$win.mbar.help add command -label "Debug" -command debug
"""


def setup():
    gui.mkcmd("settings", settings.open)
    gui.mkcmd("newtag", newtag)
    gui.mkcmd("exit", gui.task_exit)
    gui.mkcmd("debug", gui.debug)
    gui.mkcmd("save", save)
    gui.mkcmd("tagsearch", tagsearch.open)


def attach():
    gui.tclexec(tcl_code)


# Commands

def newtag():
    """Create a new tag window."""
    tag.new()
    tag.populate_default()

def save():
    settings.save_to_record()
    data.save()
    print("saved")

