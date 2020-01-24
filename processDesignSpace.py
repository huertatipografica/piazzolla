# https://github.com/googlefonts/fontmake/blob/master/tests/test_main.py
import sys
import re

from fontTools.designspaceLib import DesignSpaceDocument, RuleDescriptor, InstanceDescriptor
import defcon
from mutatorMath.ufo.document import DesignSpaceDocumentWriter, DesignSpaceDocumentReader
import os

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

file = sys.argv[1]
path = "temp/building/%s/%s.designspace" % (file, file)
minpath = "temp/building/%s/%s.Wghtmin.designspace" % (file, file)


print()
print("Generating Wghtmin ufos")
doc = DesignSpaceDocument()
doc.read(path)
mainMasters = set([m.filename for m in doc.sources])

# Interpolate MIN
if len(mainMasters) == 4:
    print()
    print("Four masters in font")

    print("New instances location for Wghtmin")
    thin = doc.instances[0]
    weight = wght.get('regular') - (wght.get('regular') - wght.get('min')) * weightCropIndex
    thin.location = {'Weight': weight, 'Optical size': optz['min']}
    thin.info = True

    black = doc.instances[8]
    weight = wght.get('regular') + (wght.get('max') - wght.get('regular')) * weightCropIndex
    black.styleName = "BlackMin"
    black.location = {'Weight': weight, 'Optical size': optz['min']}
    black.info = True

    # resetting instances
    doc.instances = []
    doc.addInstance(thin)
    doc.addInstance(black)


    doc.write(minpath)

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