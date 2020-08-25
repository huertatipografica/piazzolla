#!/usr/bin/env python

"""Routines for printing a font table."""

__author__ = 'juan@huertatipografica.com (Juan del Peral)'

import sys
from fontTools.ttLib import TTFont
from tools import dumpTable

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(
            "Wrong values. Run this script for printing a font table:\n"
            "python dumpTable.py {TTF-PATH} {TABLE-NAME}\n\n"
            "Example:\n"
            "python dumpTable.py yourFont.ttf STAT\n"
        )
    file = sys.argv[1]
    ttFont = TTFont(file)
    print(dumpTable(ttFont, sys.argv[2]))
