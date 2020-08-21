import sys
from fontTools.ttLib import TTFont
from fontTools.otlLib.builder import buildStatTable
from os.path import basename
from tools import dumpTable

file = sys.argv[1]
ttFont = TTFont(file)
isItalic = "Italic" in file

# Axes
axes = [
    dict(
        tag="opsz",
        name="Optical size",
        ordering=0,  # optional
        values=[
            dict(nominalValue=8, name='8pt'),
            dict(nominalValue=14, name='14pt'),
            dict(nominalValue=30, name='30pt', flags=0x2),
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,  # optional
        values=[
            dict(nominalValue=100, name='Thin'),
            dict(nominalValue=200, name='ExtraLight'),
            dict(nominalValue=300, name='Light', linkedValue=600),
            dict(nominalValue=400, name='Regular', linkedValue=700, flags=0x2),
            dict(nominalValue=500, name='Medium', linkedValue=800),
            dict(nominalValue=600, name='SemiBold'),
            dict(nominalValue=700, name='Bold'),
            dict(nominalValue=800, name='ExtraBold'),
            dict(nominalValue=900, name='Black'),
        ],
    ),
    dict(
        tag="ital",
        name="Italic",
        ordering=2,  # optional
        values=[dict(nominalValue=1, name='Italic')] # Italic
        if isItalic else
        [dict(nominalValue=0, name='Upright', linkedValue=1, flags=0x2)] # Upright
    ),
]


# Roman / Italic
if isItalic:
    locations = [
        dict(name='Thin Italic', location=dict(wght=100, opsz=30, ital=1)),
        dict(name='ExtraLight Italic', location=dict(wght=200, opsz=30, ital=1)),
        dict(name='Light Italic', location=dict(wght=300, opsz=30, ital=1)),
        dict(name='Italic', location=dict(wght=400, opsz=30, ital=1)),
        dict(name='Medium Italic', location=dict(wght=500, opsz=30, ital=1)),
        dict(name='SemiBold Italic', location=dict(wght=600, opsz=30, ital=1)),
        dict(name='Bold Italic', location=dict(wght=700, opsz=30, ital=1)),
        dict(name='ExtraBold Italic', location=dict(wght=800, opsz=30, ital=1)),
        dict(name='Black Italic', location=dict(wght=900, opsz=30, ital=1)),
    ]
else:
    locations = [
        dict(name='Thin', location=dict(wght=100, opsz=30, ital=0)),
        dict(name='ExtraLight', location=dict(wght=200, opsz=30, ital=0)),
        dict(name='Light', location=dict(wght=300, opsz=30, ital=0)),
        dict(name='Regular', location=dict(wght=400, opsz=30, ital=0)),
        dict(name='Medium', location=dict(wght=500, opsz=30, ital=0)),
        dict(name='SemiBold', location=dict(wght=600, opsz=30, ital=0)),
        dict(name='Bold', location=dict(wght=700, opsz=30, ital=0)),
        dict(name='ExtraBold', location=dict(wght=800, opsz=30, ital=0)),
        dict(name='Black', location=dict(wght=900, opsz=30, ital=0)),
    ]


# buildStatTable(ttFont, axes)
# buildStatTable(ttFont, axes, locations, 'Italic' if isItalic else 'Upright')
buildStatTable(ttFont, axes, None, 'Italic' if isItalic else 'Upright')
statTable = ttFont['STAT'].table

# statTable.Version = 0x00010001
# statTable.Version = 0x00010002



print()
print()
print(basename(file).upper())
print('Added STAT Table version %s.' %
      (statTable.Version))
print(dumpTable(ttFont, 'STAT'))
print(dumpTable(ttFont, 'fvar'))


ttFont.save(file)
