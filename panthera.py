"""panthera.py -- a program for curating tags


"""


import data
import gui
import menubar
import tag
import tagsearch


def run():
    data.setup()  # loads data from prior runs
    gui.setup()
    menubar.setup()
    tagsearch.setup()
    tag.setup()
    tagsearch.open()
    gui.loop()


if __name__ == "__main__":
    run()




