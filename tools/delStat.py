import sys
from fontTools.ttLib import TTFont

file = sys.argv[1]
ttFont = TTFont(file)

del ttFont["STAT"]
ttFont.save(file)
