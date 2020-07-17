import sys
from fontTools.designspaceLib import DesignSpaceDocument

file = sys.argv[1]
path = "temp/building/%s/%s.designspace" % (file, file)

doc = DesignSpaceDocument()
doc.read(path)

defaultOpsz = 30

for instance in doc.instances:
    if instance.location['Optical size'] != 30:
        instance.styleName = '%spt %s' % (
            int(instance.location['Optical size']),
            instance.styleName
        )
        print('renamed to ' + instance.styleName)


doc.write(path)