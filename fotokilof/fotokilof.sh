#!/bin/sh

# MYPATH - path to FotoKilof python source
MAIN=__main__.py
MYPATH="${0%/*}"
cd $MYPATH

# compile MO files, usable for testing tanslations
NAME=fotokilof
cd locale/
for I in ??; do
    cd $I/LC_MESSAGES
    if [ -e $NAME.po ]; then
        msgfmt $NAME.po -o $NAME.mo
    fi
    cd ../../
done
cd ..

# run FotoKilof
#python3 –m compileall $MAIN &
python3 $MAIN &

