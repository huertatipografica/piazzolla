import re
from fontParts.world import OpenFont

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

def tweakSpacing(font, offset, percentage = 0):
    for character in font:
        if character.leftMargin:
            if character.leftMargin > 0:
                character.leftMargin = character.leftMargin * ( 1 + (percentage / 100) ) + offset
            else:
                character.leftMargin = character.leftMargin + offset

            if character.rightMargin > 0:
                character.rightMargin = character.rightMargin * ( 1 + (percentage / 100) ) + offset
            else:
                character.rightMargin = character.rightMargin + offset

        else:
            character.width = character.width * ( 1 + (percentage * 2 / 100) ) + offset * 2

def removeAreas(font):
    # Delete ht _areas glyph
    for glyph in font:
        if glyph.name is '_areas':
            del font["_areas"]

def scale(source, destination, factor):

    font = OpenFont(source)
    factor = float(factor)

    font.info.descender = font.info.descender * factor
    font.info.xHeight = font.info.xHeight * factor
    font.info.capHeight = font.info.capHeight * factor
    font.info.ascender = font.info.ascender * factor
    font.info.postscriptUnderlineThickness = font.info.postscriptUnderlineThickness * factor
    font.info.postscriptUnderlinePosition = font.info.postscriptUnderlinePosition * factor

    # new PS values
    newPsValues = []
    for psValue in font.info.postscriptBlueValues:
        newPsValues.append(psValue * factor)

    font.info.postscriptBlueValues = newPsValues

    # Round everything
    font.info.round()
    # exit()

    for glyph in font:
        glyph.scaleBy(factor, None, True, True)
        for component in glyph.components:
            component.scaleBy(1/factor)

    font.save(destination)

