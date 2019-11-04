#!/bin/sh
DIST=dist
NAME="fotokilof"
OS="linux_x86_64"
VER="openSUSE-Leap-15.1"
FILES="openSUSE"
EXCLUDE="-x $FILES/locale/*/*/*.po -x $FILES/locale/fotokilof.pot -x $FILES/doc/*/*md"

echo "Files: " $FILES
echo "Exclude: " $EXCLUDE

cd ../$DIST
rm $NAME-$OS-$VER.zip
zip -r $NAME-$OS-$VER.zip $FILES $EXCLUDE

