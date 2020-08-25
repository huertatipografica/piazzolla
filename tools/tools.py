import re
from fontParts.world import OpenFont
from fontTools.misc.testTools import getXML
from fontTools.ttLib import TTFont

def parseRule(name):
    source = name.split('.rl-')[0]
    rules = re.search('(?<=.rl-)\w+', name).group(0)
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


def tweakSpacing(font, offset, percentage=0):
    for character in font:
        if character.leftMargin:
            if character.leftMargin > 0:
                character.leftMargin = character.leftMargin * \
                    (1 + (percentage / 100)) + offset
            else:
                character.leftMargin = character.leftMargin + offset

            if character.rightMargin > 0:
                character.rightMargin = character.rightMargin * \
                    (1 + (percentage / 100)) + offset
            else:
                character.rightMargin = character.rightMargin + offset

        else:
            character.width = character.width * \
                (1 + (percentage * 2 / 100)) + offset * 2


def removeAreas(font):
    # Delete ht _areas glyph
    for glyph in font:
        if glyph.name == '_areas':
            del font["_areas"]


def scaleFont(source, destination, factor):
    font = OpenFont(source)
    factor = float(factor)

    # Transform metadata
    font.info.descender = font.info.descender * factor
    font.info.xHeight = font.info.xHeight * factor
    font.info.capHeight = font.info.capHeight * factor
    font.info.ascender = font.info.ascender * factor
    font.info.postscriptUnderlineThickness = font.info.postscriptUnderlineThickness * factor
    font.info.postscriptUnderlinePosition = font.info.postscriptUnderlinePosition * factor
    font.info.postscriptBlueValues = list(
        map(lambda x: x * factor, font.info.postscriptBlueValues))

    # Transform glyphs
    for glyph in font:
        glyph.scaleBy(factor, None, True, True)
        for component in glyph.components:
            component.scaleBy(1/factor)

    # Transform kerning
    font.kerning.scaleBy(factor)

    # Round everything and save
    font.info.round()
    font.save(destination)


def dumpTable(font:TTFont, table:str):
    fontTable = font[table]
    return "\n".join(getXML(fontTable.toXML, font))