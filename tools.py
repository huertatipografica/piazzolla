import re

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

