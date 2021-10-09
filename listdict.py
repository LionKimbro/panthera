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

def req_matchall(D):
    for k,v in D.items():
        cue([D for D in g[LIST] if D[k] == v])

def req(*args, **kw):
    """Constrain down the list to meet some requirements.
    
    This can be called in several different ways.  In the example
    below, we'll cull the list down to those dictionaries that have
    D["x"] == 5.

    1. req(fn)              -- ex: req(lambda D: D["x"] == 5)
    2. req(k, fn)           -- ex: req("x", lambda x: x == 5)
    3. req(k, relation, v)  -- ex: req("x", EQ, 5)
    4. req(**kw)            -- ex: req(x=5)
    
    Or consider D["y"] > 10:

    1. req(fn)              -- ex: req(lambda D: D["y"] > 10)
    2. req(k, fn)           -- ex: req("y", lambda y: y > 10)
    3. req(k, relation, v)  -- ex: req("y", GT, 10)
    4. req(**kw)            -- CANNOT BE EXPRESSED;
                               this form can only be used for equality checks

    Or consider D["type"] == "foo" and D["name"] == "bar"

    0. (Python List Comp:)  -- ex: L = [D for D in L if D["type"] == "foo" and D["name"] == "bar"]
    1. req(fn)              -- ex: req(lambda D: D["type"] == "foo" and D["name"] == "bar")
    2. req(k, fn)           -- ex: req("type", lambda s: s=="foo")
                                   req("name", lambda s: s=="bar")
                                   (this form can only be used via serial calls)
    3. req(k, relation, v)  -- ex: req("type", EQ, "foo")
                                   req("name", EQ, "bar")
                                   (this form can only be used via serial calls)
    4. req(**kw)            -- ex: req(type="foo", name="bar")
    """
    if kw:
        req_matchall(kw)
    elif len(args) == 1:
        req_fn(*args)
    elif len(args) == 2:
        req_fn2(*args)
    elif len(args) == 3:
        req_triple(*args)
    else:
        raise TypeError


def srt(k, reverse=False):
    """Sort the list on a key."""
    g[LIST].sort(key=lambda D: D[k], reverse=reverse)


def map(x):
    """Return the result of doing something to each list item.
    
    map(fn)  --> returns result of applying fn to each item
    map(str) --> returns result of key lookup for each item
    """
    if isinstance(x, str):
        return [D[x] for D in g[LIST]]
    else:
        return [x(D) for D in g[LIST]]


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
