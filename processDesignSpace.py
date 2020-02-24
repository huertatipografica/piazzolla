import sys
import shutil
import fontmake.__main__
from fontTools.designspaceLib import DesignSpaceDocument, RuleDescriptor, InstanceDescriptor, SourceDescriptor
from tools import tweakSpacing, parseRule, removeAreas
from fontParts.world import OpenFont

# Font info
familyName = 'Piazzolla'
wght = {
    "min": 30,
    "regular": 82,
    "max": 214,
}
opsz = {
    "min": 8,
    "max": 30,
}
# Configuration
weightCropIndex = 0.5
spacing = {
    "min": {
        "offset": 15,
        "percentage": 4
    },
    "max": {
        "offset": 8,
        "percentage": 0
    },
}

# Running script
if len(sys.argv) != 2:
    print("Must specify a name:")
    print("python processDesignSpace.py PiazzollaItalic")
    exit()


file = sys.argv[1]
folder = "temp/building/%s/" % (file)
path = "temp/building/%s/%s.designspace" % (file, file)
minPath = "temp/building/%s/%s-OpszMin.designspace" % (file, file)


doc = DesignSpaceDocument()
doc.read(path)
mainMasters = set([m.filename for m in doc.sources])
if len(mainMasters) != 2:
    raise RuntimeError("File %s doesn't have 2 masters" % file)


print()
print("Mapping weight axis")
for axis in doc.axes:
    if axis.tag == 'wght':
        axis.map = [(100, 30), (200, 44), (300, 63), (400, 82),
                    (500, 100), (600, 123), (700, 153), (800, 182), (900, 214)]
        axis.default = 100
        axis.minimum = 100
        axis.maximum = 900

    if axis.tag == 'opsz':
        axis.minimum = opsz['min']


print()
print("Adding OpszMin ufos")

for ufo in set([m.path for m in doc.sources]):
    newUfo = ufo.replace('.ufo', '-OpszMin.ufo')
    shutil.copytree(ufo, newUfo)

    source = SourceDescriptor()
    source.path = newUfo
    source.familyName = familyName

    if "Light" in newUfo or "Thin" in newUfo:
        lightUfo = newUfo
        font = OpenFont(newUfo)
        tweakSpacing(font, spacing['min']['offset'],
                     spacing['min']['percentage'])
        font.save()

        source.location = {'Weight': wght['min'], 'Optical size': opsz['min']}
        source.styleName = "ThinMin"
    else:
        blackUfo = newUfo
        font = OpenFont(newUfo)
        tweakSpacing(font, spacing['max']['offset'],
                     spacing['max']['percentage'])
        font.save()

        source.location = {'Weight': wght['max'], 'Optical size': opsz['min']}
        source.styleName = "BlackMin"

    doc.addSource(source)

# removeAreas(font)
doc.write(path)
doc.write(minPath)

# Interpolate MIN
print("New instances location for OpszMin")
doc = DesignSpaceDocument()
doc.read(minPath)

# resetting instances
doc.instances = []

# Calculate location
weightMin = wght.get('regular') - (wght.get('regular') -
                                   wght.get('min')) * weightCropIndex
weightMax = wght.get('regular') + (wght.get('max') -
                                   wght.get('regular')) * weightCropIndex

instance = InstanceDescriptor()
instance.familyName = familyName
instance.styleName = "Thin"
instance.name = "Piazzolla-Thin-OpszMin.ufo"
instance.path = lightUfo
newUfo = ufo.replace('.ufo', '-OpszMin.ufo')
instance.location = {'Weight': weightMin, 'Optical size': opsz['min']}
doc.addInstance(instance)

instance = InstanceDescriptor()
instance.familyName = familyName
instance.styleName = "Black"
instance.name = "Piazzolla-Black-OpszMin.ufo"
instance.path = blackUfo
instance.location = {'Weight': weightMax, 'Optical size': opsz['min']}
doc.addInstance(instance)
doc.write(minPath)


print("Generate new ufos for OpszMin")

fontmake.__main__.main(
    [
        "-m",
        str(minPath),
        "-o",
        "ufo",
        "-i",
        "--verbose",
        "WARNING"
    ]
)


print()
print("Resetting and processing rules")
doc.rules = []

ruleNames = [r.name for r in doc.rules]
firstMaster = doc.sources[0]
font = OpenFont(firstMaster.path)
for glyph in font:
    if ".rule" in glyph.name:
        r = parseRule(glyph.name)

        # create rule
        rule = RuleDescriptor()
        rule.name = r['target']

        # add conditions
        for condition in r['conditions']:
            rule.conditionSets.append([dict(name=condition[0], minimum=float(
                condition[1]), maximum=float(condition[2]))])

        # add replacement
        rule.subs.append((r['source'], r['target']))

        doc.addRule(rule)
        print(" - Adding rule for %s -> %s" % (r['source'], r['target']))

doc.write(path)