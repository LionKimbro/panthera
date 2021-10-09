"""tagrecords.py  -- panthera tag records

Records are keyed on the following symbols:
* TAG
* TAGS
* MNEMONICS
* TITLE
* HOOK
* DESCRIPTION
* IDENTIFIER
* CREATOR
* CREATED
"""

from symbols import *

import listdict
from listdict import cue, val, val01, req, srt  # working with lists of dictionaries
from listdict import EQ, NEQ, GT, LT, GTE, LTE
from listdict import CONTAINS, NCONTAINS, WITHIN, NWITHIN


records = []


g = {REC: None}  # cursor


# Functions -- Manipulating Records Set

def find(tag):
    cue(records)
    req(TAG=tag)
    rec = g[REC] = val01()
    return rec

def delete():
    """Delete located record, if there is one."""
    if g[REC]:
        records.remove(g[REC])
        g[REC] = None

def add(rec):
    """Add (or replace) a record with this record."""
    if find(rec[TAG]):
        delete()
    records.append(rec)


# Functions -- Locating groups of tags

def tags_and_mnemonics(rec):
    tags = set(rec[TAGS])
    mnemonics = set(rec[MNEMONICS])
    return tags.union(mnemonics)

def includes_tags(rec, search_for):
    return search_for.issubset(tags_and_mnemonics(rec))


def list_tags_containing(s):
    """return list of tag records wherein tag's name contains substring
    
    s: str, substring to search for
    """
    cue(records)
    req("TAG", lambda tag: s in tag)
    srt(CREATED)
    return val()

def list_tags_tagged(s):
    """cue a list of records that are tagged by all tags listed
    
    s: str, white-space delimited tags
    """
    search_for = set(s.split())
    cue(records)
    req(lambda rec: includes_tags(rec, search_for))
    return val()


# Functions -- Debug Displays

def show():
    cue(records)
    listdict.show("TAG......... TITLE............................... CREATED.....")


# Saving and Loading

def load(data):
    """Called from data at load time, with data for this module."""
    records[:] = data

def save():
    """Called from data at save time; Supply with data to save."""
    return records

