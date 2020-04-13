Updating SCs
    Rebuild using
    Change metric groups, taking them from upper
    HT Letterspacer

Variables text order


Freezing SCs
for f in Piazzolla*; do pyftfeatfreeze -f 'smcp' -S -U SC "$f" "${f//Piazzolla/PiazzollaSC}"; done