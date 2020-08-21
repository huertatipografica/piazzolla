Spacing and metrics work
    Updating SCs
        Rebuild using
        Change metric groups, taking them from upper
        HT Letterspacer

    After change lower or uppercase
        Rebuild .sups

    Clean and compress kerning


```bash
for VF in /Library/Application\ Support/Adobe/Fonts/Piazzolla*.ttf; do
#for VF in ~/Library/Fonts/fontTest/Piazzolla*.ttf; do
    rm -f ${VF/.ttf/.ttx}
    python tools/fixNameTable.py $VF
    python tools/buildStat.py $VF
    python tools/fixNameTable.py $VF
    # ttx -t STAT $VF
done
```