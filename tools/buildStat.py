import sys
from fontTools.ttLib import TTFont
from fontTools.otlLib.builder import buildStatTable, _addName
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
            dict(nominalValue=8, rangeMinValue=8, rangeMaxValue=8, name='8pt'),
            dict(nominalValue=14, rangeMinValue=14, rangeMaxValue=14, name='14pt'),
            dict(nominalValue=30, rangeMinValue=30, rangeMaxValue=30, name='30pt', flags=0x2),
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,  # optional
        values=[
            dict(nominalValue=100, rangeMinValue=100, rangeMaxValue=150, name="Thin"),
            dict(nominalValue=200, rangeMinValue=150, rangeMaxValue=250, name="ExtraLight", linkedValue=500),
            dict(nominalValue=300, rangeMinValue=250, rangeMaxValue=350, name="Light", linkedValue=600),
            dict(nominalValue=400, rangeMinValue=350, rangeMaxValue=450, name="Regular", linkedValue=700, flags=0x2),
            dict(nominalValue=500, rangeMinValue=450, rangeMaxValue=550, name="Medium", linkedValue=800),
            dict(nominalValue=600, rangeMinValue=550, rangeMaxValue=650, name="SemiBold"),
            dict(nominalValue=700, rangeMinValue=650, rangeMaxValue=750, name="Bold"),
            dict(nominalValue=800, rangeMinValue=750, rangeMaxValue=850, name="ExtraBold"),
            dict(nominalValue=900, rangeMinValue=850, rangeMaxValue=900, name="Black"),
        ],
    ),
    dict(
        tag="ital",
        name="Italic",
        ordering=2,  # optional
        values=[
            dict(nominalValue=1, rangeMinValue=0.1, rangeMaxValue=1, name="Italic")
            if isItalic else
            dict(nominalValue=0, rangeMinValue=0, rangeMaxValue=0, name="Roman", linkedValue=1, flags=0x2),
        ]
    ),
]


def updateFvar(ttFont):
    fvar = ttFont['fvar']
    nametable = ttFont['name']
    family_name = nametable.getName(16, 3, 1, 1033) or nametable.getName(1, 3, 1, 1033)
    family_name = family_name.toUnicode().replace(" ", "")
    nametable.setName(family_name, 25, 3, 1, 1033)
    for instance in fvar.instances:
        instance_style = nametable.getName(instance.subfamilyNameID, 3, 1, 1033).toUnicode()
        ps_name = f"{family_name}-{instance_style.replace(' ', '')}"
        instance.postscriptNameID = _addName(nametable, ps_name, 256)


# buildStatTable(ttFont, axes)
buildStatTable(ttFont, axes)
updateFvar(ttFont)
statTable = ttFont['STAT'].table

## Testing STAT version change
# statTable.Version = 0x00010001
# statTable.Version = 0x00010002


print()
print()
print(basename(file).upper())
print('Added STAT Table version %s.' %
      (statTable.Version))

# Debug
print(dumpTable(ttFont, 'STAT'))
# print(dumpTable(ttFont, 'fvar'))
# print(dumpTable(ttFont, 'name'))


ttFont.save(file)
