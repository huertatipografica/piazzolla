# Piazzolla font family
![Piazzolla](extra/Piazzolla.png)

Type system intended for optimizing the available space in press media and other publications. It has a compact appearance which allows for small font sizes and tight leading while achieving solid lines and robust paragraphs.

Piazzolla has a distinctive voice that conveys a personal style, especially in display sizes. It has great performance and readability in small point sizes and long texts, both for screen and printing.

## Download

- All the fonts can be downloaded from [the releases section](/releases)


## Contribute


### Requirements

- Python 3 (for building fonts)
- Glyphs (for editing sources)


### Setup

To run any of the commands, you need to generate the virtual environment (venv) and install dependencies. It will generate the /venv folder

`python3 -m venv venv`
`. venv/bin/activate`
`pip install -r requirements.txt`


### Build ufos and generate fonts

The sources are in glyph format. To build the fonts there are several steps and all the process is being automated by running in terminal:

`sh build.sh`


### Running tests

for UFO sources
```
fontbakery check-ufo-sources --ghmarkdown bakery-report.html temp/building/*
```

for Variable Fonts
```
fontbakery check-googlefonts fonts/variable/*
```

for Static Fonts
```
fontbakery check-googlefonts fonts/static/*
```