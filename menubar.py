"""menubar.py  -- the standard menu bar for the Panthera windows"""


import data
import gui
import settings
import tagsearch
import tag


tcl_code = """
menu $top.mbar
$top configure -menu $top.mbar

menu $top.mbar.file
menu $top.mbar.new
menu $top.mbar.search
menu $top.mbar.help

$top.mbar add cascade -menu $top.mbar.file -label Panthera
$top.mbar add cascade -menu $top.mbar.new -label New
$top.mbar add cascade -menu $top.mbar.search -label Search
$top.mbar add cascade -menu $top.mbar.help -label Help

$top.mbar.file add command -label "Settings" -command settings
$top.mbar.file add separator
$top.mbar.file add command -label "Add Source"
$top.mbar.file add command -label "Save" -command save
$top.mbar.file add separator
$top.mbar.file add command -label "Exit" -command exit

$top.mbar.new add command -label "New Tag" -command newtag
$top.mbar.new add command -label "New Map"

$top.mbar.search add command -label "for Tag" -command tagsearch
$top.mbar.search add command -label "for Map"

$top.mbar.help add command -label "Tutorial"
$top.mbar.help add command -label "Contact"
$top.mbar.help add separator
$top.mbar.help add command -label "About"
$top.mbar.help add separator
$top.mbar.help add command -label "Debug" -command debug
"""


def setup():
    gui.mkcmd("settings", settings.open)
    gui.mkcmd("newtag", tag.new)
    gui.mkcmd("exit", gui.task_exit)
    gui.mkcmd("debug", gui.debug)
    gui.mkcmd("save", data.master_save)
    gui.mkcmd("tagsearch", tagsearch.open)


def attach():
    """called by gui.toplevel_unique & gui.toplevel_recurring"""
    gui.tclexec(tcl_code)

