"""entityloader.py  -- load entity package data

NOTE: the canonical version of this program is PRESENTLY (2021-10-06)
      kept in D:/repo/entityloader/entityloader.py;
  This is NOT a canonical copy.
  I haven't modified it YET, but if the last-modified date is past
  2021-10-06, there is likely a deviation here.
"""

import time
import json
import urllib.request


# Constants -- Package Files

K_FILETYPE = "$filetype"
K_PKGID = "$pkgid"
K_BLOCKS = "$blocks"

FILETYPE_PACKAGE_V1 = "tag:entitypkg.net,2022:file-type:package-v1"


# Constants -- Blocks

K_SCHEMA = "$schema"
K_TYPE = "$type"
K_EID = "$eid"

TYPE_LINK = "link"
TYPE_DATA = "data"


# Constants -- Special Keys

SK_SOURCE = "@source"  # specific source loaded from (URL or local filepath)
SK_LOADTIME = "@loadtime"  # unix utc seconds since epoch; when package began being processed
SK_PACKAGE = "@package"  # package entity id


# Constants -- Special Schema


SCH_SOURCE = "tag:entitypkg.net,2022:entity-schema:source-v1",


# Main Global Memory

blocks = []  # list of all blocks, including special keys

by_schema = {}  # idx: $schema to blocks
by_eid = {}  # idx: $eid to blocks
links = {}  # idx: entity id -> link blocks mentioning the entity id
sources = {}  # idx: entity id -> more info source schema block


# global variables

SRC="SRC"  # source identifier for the package last attempted to be received
PKGID="PKGID"  # cached package ID, for the last package received
TIME="TIME"  # cached time (unix timestamp UTC), for last package received

g = {SRC: None,
     PKGID: None,
     TIME: None}

pkg = {}  # most recently read package; the "working" package


# Functions -- Loading JSON Files

def read(src):
    if src.startswith("http://") or src.startswith("https://"):
        return read_url(src)
    else:
        return read_file(src)

def read_url(url):
    return json.load(urllib.request.urlopen(url))

def read_file(p):
    return json.load(open(p, encoding="utf-8"))


# Functions -- Loading Packages

def report_bad_package(msg):
    raise ValueError("Specified file not a package.", msg, g[SRC])

def receive_package(src):
    """Receive a package file from the Internet or local file system.
    
    Some basic checks are done to be sure that the package is sound:
    * Is it a dictionary?
    * Does it have the schema key I expect?
    * Does it have a package id?
    * Does it have a data block?
    
    g[SRC] -- before attempting to read, this is set with the src provided
    g[PKGID]  -- upon success, this is updated to the presently received package id
    g[TIME]  -- upon success, this is updated to the current time
    
    This package will be at the center of work for the time being.
    """
    g[SRC] = src
    dl = read(src)  # the download
    if not isinstance(dl, dict):
        dl_str = repr(dl)
        beginning = dl_str[:10]
        if len(dl_str) > 10:
            beginning += "..."
        msg = "the JSON data ({}) is not a JSON dictionary".format(beginning)
        report_bad_package(msg)
    pkg.clear()
    pkg.update(dl)  # OK, now I call it pkg
    s1 = K_FILETYPE
    s2 = FILETYPE_PACKAGE_V1
    if K_FILETYPE not in pkg:
        report_bad_package("the JSON data lacks {}: {}".format(s1, s2))
    if pkg[K_FILETYPE] != FILETYPE_PACKAGE_V1:
        report_bad_package("{} is {}, not {}".format(s1, pkg[K_FILETYPE], s2))
    if K_PKGID not in pkg:
        report_bad_package("the JSON data lacks {}".format(K_PKGID))
    if K_BLOCKS not in pkg:
        report_bad_package("the JSON data lacks {}".format(K_BLOCKS))
    g[PKGID] = pkg[K_PKGID]  # g[PKGID] caches the package's identifier
    g[TIME] = int(time.time())  # g[TIME] demarks the successful receipt of the package


def brand_blocks():
    for block in pkg[K_BLOCKS]:
        block[SK_SOURCE] = g[SRC]
        block[SK_LOADTIME] = g[TIME]
        block[SK_PACKAGE] = g[PKGID]

def index_by_schema():
    for block in pkg[K_BLOCKS]:
        if K_SCHEMA in block:
            schema = block[K_SCHEMA]
            by_schema.setdefault(schema, []).append(block)

def index_by_eid():
    for block in pkg[K_BLOCKS]:
        if K_EID in block:
            eid = block[K_EID]
            by_eid.setdefault(eid, []).append(block)

def index_links():
    for block in pkg[K_BLOCKS]:
        if block[K_TYPE] == TYPE_LINK:
            for eid in linkblock_terminals(block):
                links.setdefault(eid, []).append(block)

def index_sources():
    for block in pkg[K_BLOCKS]:
        if block.get(K_SCHEMA) == SCH_SOURCE:
            sources.setdefault(block[K_EID], []).append(block)


def load(src):
    receive_package(src)  # after this call: pkg, g[SRC], g[PKGID], g[TIME]
    brand_blocks()
    blocks.extend(pkg[K_BLOCKS])
    index_by_schema()
    index_by_eid()
    index_links()
    index_sources()


# Functions -- Locating terminal identifiers within link blocks

def update_list(L, additions):
    """Ordered update."""
    for x in additions:
        if x not in L:
            L.append(x)

def _helper_00(obj):
    "(set aside, to clarify recursing into 'object', not just 'block')"
    seen = []
    if isinstance(obj, dict):
        D = obj
        for (k,v) in D.items():
            if k.startswith("$") or k.startswith("@"):
                continue
            if isinstance(v, str):
                update_list(seen, [v])
            else:
                update_list(seen, _helper_00(v))
    elif isinstance(obj, list):
        L = obj
        for v in L:
            if isinstance(v, str):
                update_list(seen, [v])
            else:
                update_list(seen, _helper_00(v))
    else:
        raise ValueError("I have lost the ability to can")
    return seen

def linkblock_terminals(block):
    """Return EID terminals for a link block.
    
    The special thing about link blocks, is that their terminals are
    ALL entity identifiers.
    
    This function is a subroutine of index_links, which needs to
    collect the terminals from all link blocks, in order to inventory
    all entity identifiers referenced.
    
    Note that ALL keys that begin with punctuation are IGNORED.
    ex: $schema, $eid, @package, ...
    """
    return _helper_00(block)

