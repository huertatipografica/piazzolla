# Piazzolla font family


## Generate virtual environment
To run any of the commands, you need to generate the virtual environment (venv). It will generate the /venv folder

`source venv.sh`

## How to build fonts and sources

### UFO to glyphs
To generate your .glyph file based on .ufo sources
```
ufo2glyphs sources/Piazzolla.designspace
ufo2glyphs sources/PiazzollaItalic.designspace
```

### Glyphs to UFOs
To update .ufo sources from your .glyph file
```
glyphs2ufo sources/Piazzolla.glyphs
glyphs2ufo sources/PiazzollaItalic.glyphs
```

## Generate fonts
1. make sure you have the ufo files up to date
2. run in terminal `sh build.sh`


## Running FontBakery reports
for UFO sources
```
fontbakery check-ufo-sources --ghmarkdown bakery-report.html sources/*
```