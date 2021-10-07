"""panthera.py -- a program for curating tags


"""


import gui
import settings
import tag


def run():
    gui.setup()
    settings.setup()
    settings.open()
    tag.setup()
    gui.loop()


if __name__ == "__main__":
    run()




