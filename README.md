# Piazzolla font family
![Piazzolla](extra/Piazzolla.png)

Type system intended for optimizing the available space in press media and other publications. It has a compact appearance which allows for small font sizes and tight leading while achieving solid lines and robust paragraphs.

Piazzolla has a distinctive voice that conveys a personal style, especially in display sizes. It has great performance and readability in small point sizes and long texts, both for screen and printing.

## Download

- All the fonts can be downloaded from [the releases section](https://github.com/juandelperal/piazzolla/releases)


## Contributing

#### Requirements

- Python 3 (for building fonts)
- Glyphs (for editing sources)


#### Setup

To run any of the commands, you need to generate the virtual environment (venv) and install dependencies. It will generate a `venv` folder

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```


#### Build ufos and generate fonts

To build the fonts there are several steps and all the process is being handled by a script. All the magic happens by running in terminal:

```bash
sh build.sh
```


#### Running tests

for Variable Fonts
```bash
fontbakery check-googlefonts fonts/variable/*
```

for Static Fonts
```bash
fontbakery check-googlefonts fonts/static/*
```

for UFO sources (replace `UFO_PATH` for the ufo you want to check)
```bash
fontbakery check-ufo-sources UFO_PATH
```