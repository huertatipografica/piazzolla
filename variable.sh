#!/bin/sh
set -e

files=( Piazzolla PiazzollaItalic )

for f in $files; do
    echo
    echo Setup DesignSpace from Glyphs:
    glyphs2ufo sources/$f.glyphs -m $f
    echo
    echo Process DesignSpace:
    python processDesignSpace.py $f
    echo
    echo Update wghtmin ufos:
    fontmake -m "sources/$f.Wghtmin.designspace" -o ufo -i
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
    fontmake -m sources/$f.designspace -o variable
    # echo
    # echo "Generate static fonts for $f":
    # fontmake -m sources/$f.designspace -i
done


echo
echo Fix fonts:
for vf in variable_ttf/*.ttf; do
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

# for ttf in instance_ttf/*.ttf; do
#     gftools fix-dsig -f $ttf
#     gftools fix-nonhinting $ttf "$ttf.fix"
#     mv "$ttf.fix" $ttf
# done

# for otf in instance_otf/*.otf; do
#     gftools fix-dsig -f $otf
#     gftools fix-nonhinting $otf "$otf.fix"
#     mv "$otf.fix" $otf
# done
echo
echo Cleanup:
# rm -r sources/instance_ufos/
rm variable_ttf/*backup*.ttf
rm instance_ttf/*backup*.ttf
rm instance_otf/*backup*.otf
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
echo Order fonts:
mkdir -p fonts/static
mv variable_ttf fonts/variable
mv instance_ttf fonts/static/ttf
mv instance_otf fonts/static/otf
cp extra/Thanks.png fonts