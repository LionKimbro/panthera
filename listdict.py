"""listdict.py  -- quickly search & filter a list of dictionaries

Experimental idea, research.txt 0K2


Import with:
-----------------------------------------------------------
from listdict import cue, val, val01, req, srt
from listdict import EQ, NEQ, GT, LT, GTE, LTE
from listdict import CONTAINS, NCONTAINS, WITHIN, NWITHIN


"""


EQ="EQ"  # equal to
NEQ="NEQ"  # not equal to
GT="GT"  # greater than
LT="LT"  # less than
GTE="GTE"  # greater than or equal to
LTE="LTE"  # less than or equal to
CONTAINS="CONTAINS"  # sub-collection contains item
NCONTAINS="NCONTAINS"  # sub-collection does NOT contain item
WITHIN="WITHIN"  # value within collection
NWITHIN="NWITHIN"  # value NOT within collection


fn_mappings = {EQ: lambda a,b: a==b,
               NEQ: lambda a,b: a!=b,
               GT: lambda a,b: a>b,
               LT: lambda a,b: a<b,
               GTE: lambda a,b: a>=b,
               LTE: lambda a,b: a<=b,
               CONTAINS: lambda a,b: b in a,
               NCONTAINS: lambda a,b: b not in a,
               WITHIN: lambda a,b: a in b,
               NWITHIN: lambda a,b: a not in b}


LIST = "LIST"

g = {LIST: []}


def cue(L):
    g[LIST] = L

def val():
    return g[LIST]

def length():
    return len(g[LIST])

def val1():
    """Require that there is one item, and return it."""
    if len(g[LIST]) == 1:
        return g[LIST][0]
    else:
        raise KeyError()

def val01(default=None):
    """Require that there is zero or one item, and return it."""
    if len(g[LIST]) == 0:
        return default
    elif len(g[LIST]) == 1:
        return g[LIST][0]
    else:
        raise KeyError


def req_fn(fn):
    cue([D for D in g[LIST] if fn(D)])

def req_fn2(k, fn):
    cue([D for D in g[LIST] if fn(D[k])])

def req_triple(k, relation, v):
    fn = fn_mappings[relation]
    cue([D for D in g[LIST] if fn(D[k], v)])

def req(*args):
    if len(args) == 1:
        req_fn(*args)
    elif len(args) == 2:
        req_fn2(*args)
    elif len(args) == 3:
        req_triple(*args)
    else:
        raise TypeError


def srt(k, reverse=False):
    g[LIST].sort(key=lambda D: D[k], reverse=reverse)


def show(spec):
    """print dictionaries per a spec;
    
    example spec:
      "KEY1............. KEY2........................... KEY3......"
    
    based on snippets.py, entry DLPR: Dictionary List Print
    """
    print("NDX "+spec)
    specL = [(word.rstrip("."), len(word)) for word in spec.split()]
    for i, D in enumerate(g[LIST]):
        pieces = [str(D.get(key, "NONE")).ljust(length)[:length] for (key,length) in specL]
        print("{:>2}. ".format(i)+" ".join(pieces))
