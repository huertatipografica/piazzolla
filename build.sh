#!/bin/bash
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
    files=(Piazzolla-VARsetup Piazzolla-Italic-VARsetup)
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
    glyphs2ufo -m temp/building/$f sources/$f.glyphs
    echo "Process DesignSpace for $f"
    python tools/processDesignSpace.py $f
done

echo Generating fonts
rm -rf fonts
for f in "${files[@]}"; do
    echo
    echo "Generate variable font for $f"
    fontmake -m temp/building/$f/$f.designspace -o variable --output-dir fonts/Piazzolla/variable/ttf --verbose WARNING
    if $static; then
        echo "Generate static fonts for $f"
        fontmake -m temp/building/$f/$f.designspace -i --output-dir fonts/Piazzolla/static --verbose WARNING
    fi
done

echo
echo Fixing fonts
for VF in fonts/Piazzolla/variable/ttf/*.ttf; do
    python tools/buildStat.py $VF
    gftools fix-dsig -f $VF
    gftools fix-nonhinting $VF "$VF.fix"
    mv "$VF.fix" $VF
    ttx -f -x "MVAR" $VF
    BASE=$(basename -s .ttf $VF)
    TTXFILE=fonts/Piazzolla/variable/ttf/$BASE.ttx
    rm $VF
    ttx $TTXFILE
    rm fonts/Piazzolla/variable/ttf/$BASE.ttx
    rm fonts/Piazzolla/variable/ttf/$BASE-backup-fonttools-prep-gasp.ttf
done

if $static; then
    for ttf in fonts/Piazzolla/static/*.ttf; do
        python tools/fixNameTable.py $ttf
        gftools fix-dsig -f $ttf
        gftools fix-nonhinting $ttf "$ttf.fix"
        mv "$ttf.fix" $ttf
        ttx -f -x "MVAR" $ttf
        BASE=$(basename -s .ttf $ttf)
        TTXFILE=fonts/Piazzolla/static/$BASE.ttx
        rm $ttf
        ttx $TTXFILE
        rm fonts/Piazzolla/static/$BASE.ttx
        rm fonts/Piazzolla/static/$BASE-backup-fonttools-prep-gasp.ttf
    done

    for otf in fonts/Piazzolla/static/*.otf; do
        python tools/fixNameTable.py $VF
        gftools fix-weightclass $otf
        gftools fix-dsig -f $otf
        gftools fix-nonhinting $otf "$otf.fix"
        mv "$otf.fix" $otf
        ttx -f -x "MVAR" $otf
        BASE=$(basename -s .otf $otf)
        TTXFILE=fonts/Piazzolla/static/$BASE.ttx
        rm $otf
        ttx $TTXFILE
        rm fonts/Piazzolla/static/$BASE.ttx
        rm fonts/Piazzolla/static/$BASE-backup-fonttools-prep-gasp.otf
    done
fi

echo
echo Order files

for ttf in fonts/Piazzolla/variable/ttf/*.ttf; do
    mv $ttf ${ttf/-VARsetup/''}
done

if $static; then
    mkdir -p fonts/Piazzolla/static/ttf
    mkdir -p fonts/Piazzolla/static/otf
    mv fonts/Piazzolla/static/*.otf fonts/Piazzolla/static/otf
    mv fonts/Piazzolla/static/*.ttf fonts/Piazzolla/static/ttf
fi
for f in fonts/Piazzolla/variable/ttf/*-VF*; do mv "$f" "${f//-VF/[opsz,wght]}"; done
cp extra/Thanks.png fonts/Piazzolla
cp OFL.txt fonts/Piazzolla

echo
echo Freezing Small Caps
rm -rf fonts/PiazzollaSC
cp -r fonts/Piazzolla fonts/PiazzollaSC
cd fonts/PiazzollaSC
for f in variable/ttf/*; do echo && echo Freezing SC version for "$f" && pyftfeatfreeze -f 'smcp' -S -U SC "$f" "${f//Piazzolla/PiazzollaSC}" && rm "$f"; done
if $static; then
    for f in static/otf/*; do echo && echo Freezing SC version for "$f" && pyftfeatfreeze -f 'smcp' -S -U SC "$f" "${f//Piazzolla/PiazzollaSC}" && rm "$f"; done
    for f in static/ttf/*; do echo && echo Freezing SC version for "$f" && pyftfeatfreeze -f 'smcp' -S -U SC "$f" "${f//Piazzolla/PiazzollaSC}" && rm "$f"; done
fi
cd ../..

echo
echo Generate woff2 files
if $static; then
    for ttf in fonts/Piazzolla/static/ttf/*.ttf; do
        mkdir -p fonts/Piazzolla/static/woff2
        fonttools ttLib.woff2 compress $ttf
        mv ${ttf/.ttf/.woff2} fonts/Piazzolla/static/woff2
    done
    for ttf in fonts/PiazzollaSC/static/ttf/*.ttf; do
        mkdir -p fonts/PiazzollaSC/static/woff2
        fonttools ttLib.woff2 compress $ttf
        mv ${ttf/.ttf/.woff2} fonts/PiazzollaSC/static/woff2
    done
fi

for ttf in fonts/Piazzolla/variable/ttf/*.ttf; do
    mkdir -p fonts/Piazzolla/variable/woff2
    fonttools ttLib.woff2 compress $ttf
    mv ${ttf/.ttf/.woff2} fonts/Piazzolla/variable/woff2
    cp fonts/Piazzolla/variable/woff2/* extra/assets
done

for ttf in fonts/PiazzollaSC/variable/ttf/*.ttf; do
    mkdir -p fonts/PiazzollaSC/variable/woff2
    fonttools ttLib.woff2 compress $ttf
    mv ${ttf/.ttf/.woff2} fonts/PiazzollaSC/variable/woff2
done
