#!/bin/sh

# MYPATH - path to FotoKilof python source
MAIN=__main__.py
MYPATH="${0%/*}"
cd $MYPATH

# compile MO files, usable for testing tanslations
NAME=fotokilof
for L in locale/??; do
    if [ -e $L/LC_MESSAGES/$NAME.po ]; then
        msgfmt $L/LC_MESSAGES/$NAME.po -o $L/LC_MESSAGES/$NAME.mo
    fi
done

# run FotoKilof
#python3 –m compileall $MAIN &
python3 $MAIN &

