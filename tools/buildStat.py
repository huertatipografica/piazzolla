import sys
from fontTools.ttLib import TTFont
from fontTools.otlLib.builder import buildStatTable

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
            dict(value=300, name='Light', linkedValue=600),
            dict(value=400, name='Regular', linkedValue=700, flags=0x2),
            dict(value=500, name='Medium', linkedValue=800),
            dict(value=600, name='SemiBold'),
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

# Locations
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


buildStatTable(ttFont, axes, locations, 'Italic' if isItalic else 'Upright')
ttFont.save(file)
