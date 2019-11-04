#!/bin/sh
DIST=dist
NAME="fotokilof"
OS="linux_x86_64"
VER="Ubuntu-19.10"
FILES="Ubuntu"
EXCLUDE="-x $FILES/locale/*/*/*.po -x $FILES/locale/fotokilof.pot -x $FILES/doc/*/*md"

echo "Files: " $FILES
echo "Exclude: " $EXCLUDE

cd ../$DIST
zip -r $NAME-$OS-$VER.zip $FILES $EXCLUDE
