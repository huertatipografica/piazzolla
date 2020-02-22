from fontParts.world import OpenFont

files = [
    {
        'path': 'temp/Piazzolla-Thin.ufo',
        'newPath': 'temp/Piazzolla-Thin-space.ufo',
        'offset': 22,
        'percentage': 3,
    },
    {
        'path': 'temp/Piazzolla-Black.ufo',
        'newPath': 'temp/Piazzolla-Black-space.ufo',
        'offset': 17,
        'percentage': 0,
    }
]

for file in files:
    font = OpenFont(file['path'])
    offset = file['offset']
    percentage = file['percentage']

    for character in font:
        if character.leftMargin:
            character.leftMargin = character.leftMargin * ( 1 + (percentage / 100) ) + offset
            character.rightMargin = character.rightMargin * ( 1 + (percentage / 100) ) + offset
        else:
            character.width = character.width * ( 1 + (percentage * 2 / 100) ) + offset * 2

    font.save(file['newPath'])