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
    "regular": 80,
    "max": 208,
}
opsz = {
    "min": 8,
    "max": 30,
}
# Configuration
weightCropIndex = 0.5
adjustments = {
    "min": {
        "offset": 15,
        "percentage": 4,
        "scaleFactor": 1
    },
    "max": {
        "offset": 8,
        "percentage": 0,
        "scaleFactor": 1
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
        axis.map = [(100, 30), (200, 45), (300, 62), (400, 80),
                    (500, 99), (600, 120), (700, 149), (800, 177), (900, 208)]
        axis.default = 100
        axis.minimum = 100
        axis.maximum = 900

    if axis.tag == 'opsz':
        axis.minimum = opsz['min']


print()
print("Processing OpszMin")

for ufo in set([m.path for m in doc.sources]):
    newUfo = ufo.replace('.ufo', '-OpszMin.ufo')
    shutil.copytree(ufo, newUfo)

    source = SourceDescriptor()
    source.path = newUfo
    source.familyName = familyName

    if "Light" in newUfo or "Thin" in newUfo:
        lightUfo = newUfo
        font = OpenFont(newUfo)
        tweakSpacing(font, adjustments['min']['offset'],
                     adjustments['min']['percentage'])
        font.save()

        source.location = {'Weight': wght['min'], 'Optical size': opsz['min']}
        source.styleName = "ThinMin"
    else:
        blackUfo = newUfo
        font = OpenFont(newUfo)
        tweakSpacing(font, adjustments['max']['offset'],
                     adjustments['max']['percentage'])
        font.save()

        source.location = {'Weight': wght['max'], 'Optical size': opsz['min']}
        source.styleName = "BlackMin"

    doc.addSource(source)

# removeAreas(font)
doc.write(path)
doc.write(minPath)

minDoc = DesignSpaceDocument()
minDoc.read(minPath)

# resetting instances
minDoc.instances = []

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
minDoc.addInstance(instance)

instance = InstanceDescriptor()
instance.familyName = familyName
instance.styleName = "Black"
instance.name = "Piazzolla-Black-OpszMin.ufo"
instance.path = blackUfo
instance.location = {'Weight': weightMax, 'Optical size': opsz['min']}
minDoc.addInstance(instance)
minDoc.write(minPath)


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