#!/bin/sh

files=(PiazzollaVARsetup PiazzollaVARsetupItalic)
# files=(Piazzolla PiazzollaItalic)

for f in "${files[@]}"; do
    echo Setup DesignSpace from Glyphs
    if [ -e temp/building/$f ]; then rm -rf temp/building/$f; fi
    mkdir -p temp/building/$f
    glyphs2ufo sources/$f.glyphs -m temp/building/$f
    echo Process DesignSpace
    python tools/processDesignSpace.py $f
done

echo Generating fonts
for f in "${files[@]}"; do
    echo "Generate variable fonts for $f"
    fontmake -m temp/building/$f/$f.designspace -o variable --output-dir fonts/variable --verbose WARNING
    echo "Generate static fonts for $f"
    fontmake -m temp/building/$f/$f.designspace -i --output-dir fonts/static --verbose WARNING
done

echo Fixing fonts
for VF in fonts/variable/*.ttf; do
    gftools fix-dsig -f $VF
    gftools fix-nonhinting $VF "$VF.fix"
    mv "$VF.fix" $VF
    ttx -f -x "MVAR" $VF
    BASE=$(basename -s .ttf $VF)
    TTXFILE=fonts/variable/$BASE.ttx
    rm $VF
    ttx $TTXFILE
    rm fonts/variable/$BASE.ttx
    rm fonts/variable/$BASE-backup-fonttools-prep-gasp.ttf
done

for ttf in fonts/static/*.ttf; do
    gftools fix-dsig -f $ttf
    gftools fix-nonhinting $ttf "$ttf.fix"
    mv "$ttf.fix" $ttf
    ttx -f -x "MVAR" $ttf
    BASE=$(basename -s .ttf $ttf)
    TTXFILE=fonts/static/$BASE.ttx
    rm $ttf
    ttx $TTXFILE
    rm fonts/static/$BASE.ttx
    rm fonts/static/$BASE-backup-fonttools-prep-gasp.ttf
done

for otf in fonts/static/*.otf; do
    gftools fix-dsig -f $otf
    gftools fix-nonhinting $otf "$otf.fix"
    mv "$otf.fix" $otf
    ttx -f -x "MVAR" $otf
    BASE=$(basename -s .otf $otf)
    TTXFILE=fonts/static/$BASE.ttx
    rm $otf
    ttx $TTXFILE
    rm fonts/static/$BASE.ttx
    rm fonts/static/$BASE-backup-fonttools-prep-gasp.otf
done

# echo Check sources
# mkdir -p tests
# cd tests
# fontbakery check-ufo-sources --ghmarkdown ufo-report.md ../sources/*
# echo Check variable fonts
# fontbakery check-universal --ghmarkdown variable-report.md ../fonts/variable/*
# echo Check static ttfs
# fontbakery check-universal --ghmarkdown ttfs-report.md ../instance_ttf/*
# echo Check static otfs
# fontbakery check-universal --ghmarkdown otfs-report.md ../instance_otf/*echo Order files

echo Files order
mkdir -p fonts/static/ttf
mkdir -p fonts/static/otf
mv fonts/static/*.otf fonts/static/otf
mv fonts/static/*.ttf fonts/static/ttf
cp extra/Thanks.png fonts


