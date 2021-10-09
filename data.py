"""data.py  -- panthera data storage and retrieval"""

import json

import listdict
from listdict import cue, val, val01, req, srt  # working with lists of dictionaries
from listdict import EQ, NEQ, GT, LT, GTE, LTE
from listdict import CONTAINS, NCONTAINS, WITHIN, NWITHIN

import tag  # tag window


class Impossible(Exception): pass


records = []


# record type
TYPE="TYPE"; TAG="TAG"; MAP="MAP"; SETTINGS="SETTINGS"


# Setup

def setup():
    load()


# Settings Information Retrieval and Storage

def settings_record():
    """Locate or create a SETTINGS record."""
    cue(records)
    req(TYPE, EQ, SETTINGS)
    D = val01()
    if D is None:
        D = {TYPE: SETTINGS}
        records.append(D)
    return D


# Functions -- Adding, locating, and removing tags

def add_tag():
    remove_tag_if_present(tag.h[TAG])
    tag_to_record()

def find_tag(tag):
    cue(records)
    req(TYPE, EQ, TAG)
    req(TAG, EQ, tag)
    return val01()

def remove_tag_if_present(tag):
    D = find_tag(tag)
    if D:
        records.remove(D)


# Functions -- Locating groups of tags

def includes_tags(rec, tag_set):
    rec_set = set(rec["TAGS"]).union(set(rec["MNEMONICS"]))
    return tag_set.issubset(rec_set)

def list_tags_containing(s):
    """cue a list of records that have tags containing this substring
    
    s: a string that is a tag substring to search for
    """
    cue(records)
    req(TYPE, EQ, TAG)
    req("TAG", lambda tag: s in tag)
    srt("TAG")
    return val()

def list_tags_tagged(s):
    """cue a list of records that are tagged by all tags listed
    
    s: a string that is a white-space delimited list of tags
    """
    tag_set = set(s.split())
    cue(records)
    req(TYPE, EQ, TAG)
    req(lambda rec: includes_tags(rec, tag_set))
    return val()


# Functions -- Moving between a tag record and tag.py's "h" dictionary

def tag_to_record():
    """Create a NEW record from tag's "h" dictionary."""
    D = tag.h.copy()
    D[TYPE] = TAG
    records.append(D)

def record_to_tag(D):
    """Populate tag's "h" dictionary from a found record D."""
    D2 = D.copy()
    del D2[TYPE]
    tag.h.update(D2)


# Functions -- Primitive File Access

def save():
    json.dump(records, open("records.txt", "w", encoding="utf-8"), indent=2)

def load():
    L = json.load(open("records.txt", "r", encoding="utf-8"))
    records[:] = L

def show():
    cue(records)
    listdict.show("TYPE................")

