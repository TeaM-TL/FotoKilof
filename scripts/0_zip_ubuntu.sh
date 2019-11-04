#!/bin/sh
DIST=dist
NAME="fotokilof"
OS="linux_x86_64"
VER="Ubuntu-18.04.3"
FILES="Ubuntu"
EXCLUDE="-x $FILES/locale/*/*/*.po -x $FILES/locale/fotokilof.pot -x $FILES/doc/*/*md"

echo "Files: " $FILES
echo "Exclude: " $EXCLUDE

cd ../$DIST
rm $NAME-$OS-$VER.zip
zip -r $NAME-$OS-$VER.zip $FILES $EXCLUDE

