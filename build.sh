#!/bin/sh
echo
echo Usage:
echo build.sh [--test] [--no-static]
echo

inArray() {
    local e match="$1"
    shift
    for e; do [[ "$e" == "$match" ]] && return 0; done
    return 1
}

if inArray "--test" $@; then
    files=(PiazzollaVARsetup PiazzollaVARsetup-Italic)
else
    files=(Piazzolla Piazzolla-Italic)
fi

if inArray "--no-static" $@; then
    static=false
else
    static=true
fi

for f in "${files[@]}"; do
    echo "Setup DesignSpace from Glyphs for $f"
    if [ -e temp/building/$f ]; then rm -rf temp/building/$f; fi
    mkdir -p temp/building/$f
    glyphs2ufo sources/$f.glyphs -m temp/building/$f
    echo "Process DesignSpace for $f"
    python tools/processDesignSpace.py $f
done

echo Generating fonts
for f in "${files[@]}"; do
    echo "Generate variable fonts for $f"
    fontmake -m temp/building/$f/$f.designspace -o variable --output-dir fonts/variable --verbose WARNING
    if $static; then
        echo "Generate static fonts for $f"
        fontmake -m temp/building/$f/$f.designspace -i --output-dir fonts/static --verbose WARNING
    fi
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

if $static; then
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
fi

echo Files order
if $static; then
    mkdir -p fonts/static/ttf
    mkdir -p fonts/static/otf
    mv fonts/static/*.otf fonts/static/otf
    mv fonts/static/*.ttf fonts/static/ttf
fi
for f in fonts/variable/*-VF*; do mv "$f" "${f//-VF/[opsz,wght]}"; done
cp extra/Thanks.png fonts
