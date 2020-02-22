# https://github.com/googlefonts/fontmake/blob/master/tests/test_main.py
import sys
import re
import os
import defcon
import shutil
import fontmake
from fontTools.designspaceLib import DesignSpaceDocument, RuleDescriptor, InstanceDescriptor
from fontParts.world import OpenFont



if len(sys.argv) != 2:
    print("Must specify a name:")
    print("python processDesignSpace.py PiazzollaItalic")
    exit()


wght = {
    "min": 30,
    "regular": 82,
    "max": 214,

}
optz = {
    "min": 8,
    "max": 36,
}

weightCropIndex = 0.5


def parseRule(name):
    source = name.split('.rule-')[0]
    rules = re.search('(?<=.rule-)\w+', name).group(0)
    rules = rules.split('.')
    conditions = []

    for rule in rules:
        condition = rule.split('_')
        conditions.append(condition)

    return {
        'source': source,
        'target': name,
        'conditions': conditions
    }

def tweakSpacing(path, offset, percentage = 0):
    font = OpenFont(path)
    for character in font:
        if character.leftMargin:
            character.leftMargin = character.leftMargin * ( 1 + (percentage / 100) ) + offset
            character.rightMargin = character.rightMargin * ( 1 + (percentage / 100) ) + offset
        else:
            character.width = character.width * ( 1 + (percentage * 2 / 100) ) + offset * 2
    font.save()


file = sys.argv[1]
path = "temp/building/%s/%s.designspace" % (file, file)
minPath = "temp/building/%s/%s.WghtMin.designspace" % (file, file)


print()
print("Generating Wghtmin ufos")
doc = DesignSpaceDocument()
doc.read(path)
mainMasters = set([m.filename for m in doc.sources])
if len(mainMasters) != 2:
    raise RuntimeError("File %s doesn't have 2 masters" % file)

for ufo in set([m.path for m in doc.sources]):
    newUfo = ufo.replace('.ufo', '.WghtMin.ufo')
    shutil.copytree(ufo, newUfo)
    if "Light" in newUfo or "Thin" in newUfo:
        tweakSpacing(newUfo, 24, 4)
    else:
        tweakSpacing(newUfo, 17, 0)


print(len(mainMasters))
for source in doc.sources:
    print(source.path, source.location)
exit()
# Interpolate MIN

print()
print("Duplicate masters")

print("New instances location for Wghtmin")
thin = doc.instances[0]
weight = wght.get('regular') - (wght.get('regular') - wght.get('min')) * weightCropIndex
thin.location = {'Weight': weight, 'Optical size': optz['min']}

black = doc.instances[8]
weight = wght.get('regular') + (wght.get('max') - wght.get('regular')) * weightCropIndex
black.styleName = "BlackMin"
black.location = {'Weight': weight, 'Optical size': optz['min']}

# resetting instances
doc.instances = []
doc.addInstance(thin)
doc.addInstance(black)


doc.write(minPath)

fontmake.__main__.main(
    [
        "-m",
        str(minPath),
        "-o",
        "ufo",
        "-i",
    ]
)

# Space
print()
print("Processing %s:" % (path))
doc = DesignSpaceDocument()
doc.read(path)

print()
print("Mapping weight axis")
for axis in doc.axes:
    if axis.tag == 'wght':
        axis.map = [(100, 30), (200, 44), (300, 63), (400, 82),
                    (500, 100), (600, 123), (700, 153), (800, 182), (900, 214)]
        axis.default = 100
        axis.minimum = 100
        axis.maximum = 900

print()
print("Resetting and processing rules")
doc.rules = []

ruleNames = [ r.name for r in doc.rules]
firstMaster = doc.sources[0]
font = defcon.Font(firstMaster.path)
for glyph in font:
    if ".rule" in glyph.name:
        r = parseRule(glyph.name)

        # create rule
        rule = RuleDescriptor()
        rule.name = r['target']

        # add conditions
        for condition in r['conditions']:
            rule.conditionSets.append([dict(name=condition[0], minimum=float(condition[1]) , maximum=float(condition[2]))])

        # add replacement
        rule.subs.append((r['source'], r['target']))

        doc.addRule(rule)
        print(" - Adding rule for %s -> %s" % (r['source'], r['target']))

doc.write(path)





# for ufo in doc.sources:
#     font = defcon.Font(ufo)
#     doc = DesignSpaceDocument()
#     doc.read(font)

#     for glyph in font:
#         # Delete ht _areas glyph
#         if glyph.name is '_areas':
#             del font["_areas"]
#     doc.write(path)