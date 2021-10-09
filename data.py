"""data.py  -- panthera master data storage and retrieval"""

import json

import settings
import tagrecords


# Setup

def setup():
    master_load()


# Functions -- Primitive File Access

def master_save():
    data = [settings.save(), tagrecords.save()]
    json.dump(data, open("db.txt", "w", encoding="utf-8"), indent=2)

def master_load():
    data = json.load(open("db.txt", "r", encoding="utf-8"))
    settings.load(data[0])
    tagrecords.load(data[1])

