"""symbols.py  -- global symbols list for panthera

Lion:
  I don't like getting errors due to mis-spelled symbols in quotation
  marks.  Defining symbols like this, means that an unidentified key
  will be identified right away, showing up as a NameError.  It also
  creates some brevity, as quotation marks are not required: TAG vs
  "TAG".

  However, then there is this issue of foo.fn(foo.SYMBOL).  My
  solution is to make symbols universal to the program, so that "from
  symbols import *" is commonplace, and therefor only foo.fn(SYMBOL)
  is required.

  I also use symbols to simplify.  I re-use symbols, and use simpler
  symbols, rather than forming deep hierarchical taxonomies.  I think
  a bit (but not too hard) before deciding to add a new symbol.

  This *does* make it harder to search for the one unique component
  that you are looking for, which is a cost, ... ...but I choose to
  pay that cost, in exchange for the simpler text.

  When I must interoperate with outside systems with lengthy keys, I
  have a translation layer within a module that converts the symbols
  of my program, to the more sophisticated lengthy keys from outside.
"""

AUTHORITY="AUTHORITY"
CONTAINS="CONTAINS"
CREATED="CREATED"
CREATOR="CREATOR"
DESCRIPTION="DESCRIPTION"
DICT="DICT"
ENTRY="ENTRY"
FN="FN"
HANDLE="HANDLE"
HOOK="HOOK"
IDENTIFIER="IDENTIFIER"
KIND="KIND"
LISTBOX="LISTBOX"
LOOP="LOOP"
MAP="MAP"  # not used yet
MAPPING="MAPPING"
MAPS="MAPS"  # not used yet
MAPSEARCH="MAPSEARCH"  # not used yet
MNEMONICS="MNEMONICS"
NEXTID="NEXTID"
PATTERN="PATTERN"
REC="REC"  # short for "record"
REQUEST="REQUEST"
RESULT="RESULT"
SETTINGS="SETTINGS"
STR="STR"
STRLIST="STRLIST"
TAG="TAG"
TAGS="TAGS"
TAGSEARCH="TAGSEARCH"
TCL="TCL"
TEXT="TEXT"
TITLE="TITLE"
TKNAME="TKNAME"
TYPE="TYPE"
UNIQUE="UNIQUE"
USER="USER"
WITH="WITH"


