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
    python tools/buildStat.py $VF
done
```

```python
for layer in Font.selectedLayers:
	x = 0
	newPath = GSPath()
	for i in Font.instances:
		newNode = GSNode()
		newNode.type = GSLINE
		newNode.position = ( x, i.weightValue )

		newPath.addNode_(newNode)
		x += 20
		print(i.weightValue)

	layer.paths.append( newPath )
```