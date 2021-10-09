"""util.py  -- miscellaneous utility functions"""


# Functions -- path into dictionary: getting, setting

def path_set(D, p, val):
    for k in p[:-1]:
        D = D[k]
    D[p[-1]] = val

def path_get(D, p):
    for k in p[:-1]:
        D = D[k]
    return D[p[-1]]

