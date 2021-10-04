"""
Settings window:

- user's own tag,
- user's authority (e-mail addr or domain)
- prefix for default new tag identifiers
  ("%AUTH" for user's authority, "%YEAR" "%MONTH" or "%DAY%" for the current day's date,)

...and a help button next to each for hover-over explanations about each...

     0                  1
   +------------------+-----------------------------------
  0| User's Tag:      | [ttk::entry] -- ($win.utag.var)
   | $win.utaglbl     | $win.utag      
   +------------------+-----------------------------------
  1| $win.utagexplain (ttk::label)
   +------------------+-----------------------------------
  2| User's Authority:| [ttk::entry] -- ($win.uauth.var)
   | $win.uauthlbl    | $win.uauth
   +------------------+-----------------------------------
  3| $win.uauthexplain (ttk::label)
   +------------------+-----------------------------------
  4| New Tag Prefix:  | [ttk::entry] -- ($win.prefix.var)
   | $win.prefixlbl   | $win.prefix
   +------------------+-----------------------------------
  5| $win.prefixexplain (ttk::label)
   +------------------+-----------------------------------
  6| [tk::text $win.explanation -height 3]
   |                  .
   +------------------+-----------------------------------

"""

import tkinter as tk


tcl_code = """
wm withdraw .

set win ".settings"
toplevel $win

ttk::label $win.utaglbl -text "User's Tag:"
grid $win.utaglbl -row 0 -column 0 -sticky e -padx "10 5" -pady "10 5"

ttk::entry $win.utag -textvariable $win.utag.var
grid $win.utag -row 0 -column 1 -sticky ew -padx "0 10" -pady "10 5"

ttk::label $win.utagexplain -text "This is the RFC 4151 Tag URI for the user, and it should begin with 'tag:'."
grid $win.utagexplain -row 1 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"

set $win.utag.var "tag:lionkimbro@gmail.com,2022:person:lion"


ttk::label $win.uauthlbl -text "User's Authority:"
grid $win.uauthlbl -row 2 -column 0 -sticky e -padx "10 5" -pady 5

ttk::entry $win.uauth -textvariable $win.uauth.var
grid $win.uauth -row 2 -column 1 -sticky ew -padx "0 10" -pady 5

ttk::label $win.uauthexplain -text "This is either an e-mail address, or a domain name, that the user controls."
grid $win.uauthexplain -row 3 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"

set $win.uauth.var "lionkimbro@gmail.com"


ttk::label $win.tagidformlbl -text "Tag Identifier Form:"
grid $win.tagidformlbl -row 4 -column 0 -sticky e -padx "10 5" -pady 5

ttk::entry $win.tagidform -textvariable $win.tagidform.var
grid $win.tagidform -row 4 -column 1 -sticky ew -padx "0 10" -pady 5

ttk::label $win.tagidformexplain -text "The form of a user tag.  It should probably be: %AUTH,%DAY:tag:%TAG, but could also use %MONTH or %YEAR."
grid $win.tagidformexplain -row 5 -column 0 -columnspan 2 -sticky w -padx 10 -pady "0 5"

set $win.tagidform.var "%AUTH,%DAY:tag:%TAG"


grid columnconfigure $win 0 -weight 0
grid columnconfigure $win 1 -weight 1


menu $win.mbar
$win configure -menu $win.mbar

menu $win.mbar.file
menu $win.mbar.new
menu $win.mbar.search
menu $win.mbar.help

$win.mbar add cascade -menu $win.mbar.file -label File
$win.mbar add cascade -menu $win.mbar.new -label New
$win.mbar add cascade -menu $win.mbar.search -label Search
$win.mbar add cascade -menu $win.mbar.help -label Help

$win.mbar.file add command -label "Add"
$win.mbar.file add command -label "Forget"
$win.mbar.file add separator
$win.mbar.file add command -label "Save"
$win.mbar.file add command -label "Save To"
$win.mbar.file add separator
$win.mbar.file add command -label "Exit"

$win.mbar.new add command -label "New Tag"
$win.mbar.new add command -label "New Map"

$win.mbar.search add command -label "for Tag"
$win.mbar.search add command -label "for Map"

$win.mbar.help add command -label "Tutorial"
$win.mbar.help add command -label "Contact"
$win.mbar.help add separator
$win.mbar.help add command -label "About"


wm protocol $win WM_DELETE_WINDOW closed
"""

root = tk.Tk()

utag = tk.StringVar(name=".settings.utag.var")
uauth = tk.StringVar(name=".settings.uauth.var")
tagidform = tk.StringVar(name=".settings.tagidform.var")

def focused():
    return root.tk.eval("focus")

def closed():
    print("window closed ({})".format(focused()))
    root.destroy()

root.tk.eval(tcl_code)

print(utag.get())
print(uauth.get())
print(tagidform.get())

root.tk.createcommand("closed", closed)


root.mainloop()

