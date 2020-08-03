import sys
from fontTools.ttLib import TTFont
from fontTools.otlLib.builder import buildStatTable

file = sys.argv[1]
ttFont = TTFont(file)
isItalic = "Italic" in file

axes = [
    dict(
        tag="opsz",
        name="Optical size",
        ordering=0,  # optional
        values=[
            dict(value=8, name='8pt'),
            dict(value=14, name='14pt'),
            dict(value=30, name='30pt', flags=0x2),
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,  # optional
        values=[
            dict(value=100, name='Thin'),
            dict(value=200, name='ExtraLight'),
            dict(value=300, name='Light', linkedValue=700),
            dict(value=400, name='Regular', linkedValue=700, flags=0x2),
            dict(value=500, name='Medium', linkedValue=800),
            dict(value=600, name='SemiBold', linkedValue=900),
            dict(value=700, name='Bold'),
            dict(value=800, name='ExtraBold'),
            dict(value=900, name='Black'),
        ],
    ),
    dict(
        tag="ital",
        name="Italic",
        ordering=2,  # optional
        values=[
            dict(value=0, name='Upright', linkedValue=1, flags=0x2),
            dict(value=1, name='Italic'),
        ],
    ),
]

buildStatTable(ttFont, axes, None, 'Italic' if isItalic else 'Upright')
ttFont.save(file)
