#!/bin/sh

files=( PiazzollaItalic )

for f in $files; do
    echo
    echo Setup DesignSpace from Glyphs:
    mkdir -p temp/building/$f
    glyphs2ufo sources/$f.glyphs -m temp/building/$f
    echo
    echo Process DesignSpace:
    python processDesignSpace.py $f
    # echo
    # echo Update wghtmin ufos:
    # fontmake -m "temp/building/$f/$f.Wghtmin.designspace" -o ufo -i
done

# echo
# echo Replace ufos:
# rm -r sources/Piazzolla-BlackMin.ufo
# rm -r sources/Piazzolla-ThinMin.ufo
# mv sources/instance_ufos/Piazzolla-Black.ufo sources/Piazzolla-BlackMin.ufo
# mv sources/instance_ufos/Piazzolla-Thin.ufo sources/Piazzolla-ThinMin.ufo
# rm -r sources/Piazzolla-BlackMinItalic.ufo
# rm -r sources/Piazzolla-ThinMinItalic.ufo
# mv sources/instance_ufos/Piazzolla-Black.ufo sources/Piazzolla-BlackMinItalic.ufo
# mv sources/instance_ufos/Piazzolla-Thin.ufo sources/Piazzolla-ThinMinItalic.ufo


for f in $files; do
    echo
    echo "Generate variable fonts for $f":
    fontmake -m temp/building/$f/$f.designspace -o variable --output-dir fonts/variable
    # echo
    # echo "Generate static fonts for $f":
    # fontmake -m sources/$f.designspace -i --output-dir fonts/static
done

echo
echo Fix fonts:
for vf in fonts/variable/*.ttf; do
    gftools fix-dsig -f $vf
    gftools fix-nonhinting $vf "$vf.fix"
    mv "$vf.fix" $vf
    ttx -f -x "MVAR" $vf
    rtrip=$(basename -s .ttf $vf)
    new_file=variable_ttf/$rtrip.ttx
    rm $vf
    ttx $new_file
    rm variable_ttf/*.ttx
done

# for ttf in fonts/static/*.ttf; do
#     gftools fix-dsig -f $ttf
#     gftools fix-nonhinting $ttf "$ttf.fix"
#     mv "$ttf.fix" $ttf
# done

# for otf in fonts/static/*.otf; do
#     gftools fix-dsig -f $otf
#     gftools fix-nonhinting $otf "$otf.fix"
#     mv "$otf.fix" $otf
# done

# echo
# echo Check sources:
# mkdir -p tests
# cd tests
# fontbakery check-ufo-sources --ghmarkdown ufo-report.md ../sources/*
# echo
# echo Check variable fonts:
# fontbakery check-universal --ghmarkdown variable-report.md ../variable_ttf/*
# echo
# echo Check static ttfs:
# fontbakery check-universal --ghmarkdown ttfs-report.md ../instance_ttf/*
# echo
# echo Check static otfs:
# fontbakery check-universal --ghmarkdown otfs-report.md ../instance_otf/*
echo
echo Order files:
cp extra/Thanks.png fonts