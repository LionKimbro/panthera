"""data.py  -- panthera data storage and retrieval"""

import json

from listdict import cue, val, val01, req, srt  # working with lists of dictionaries
from listdict import EQ, NEQ, GT, LT, GTE, LTE
from listdict import CONTAINS, NCONTAINS, WITHIN, NWITHIN

import tag  # tag window


class Impossible(Exception): pass


records = []


# record type
TYPE="TYPE"; TAG="TAG"; MAP="MAP"


# Common Operations

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


def tag_to_record():
    D = tag.h.copy()
    D[TYPE] = TAG
    records.append(D)

def record_to_tag(D):
    D2 = D.copy()
    del D2[TYPE]
    tag.h.update(D2)


# Primitive File Access

def save():
    json.dump(records, open("records.txt", "w", encoding="utf-8"), indent=2)

def load():
    L = json.load(open("records.txt", "r", encoding="utf-8"))
    records[:] = L

