#!/usr/bin/env python

"""Routines for scaling a font."""

__author__ = 'juan@huertatipografica.com (Juan del Peral)'

import sys
from tools import scaleFont

if __name__ == "__main__":
    if len(sys.argv) is not 4:
        exit(
            "Wrong values. Run this script for scaling a font:\n"
            "python scale.py sourceFont.ufo newFont.ufo 1.2\n"
        )
    scaleFont(sys.argv[1], sys.argv[2], sys.argv[3])
