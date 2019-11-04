#!/bin/sh
DIST=dist
NAME="fotokilof"
OS="windows_x64"
VER="8.1"
FILES="Windows"
EXCLUDE="-x $FILES/locale/*/*/*.po -x $FILES/locale/fotokilof.pot -x  $FILES/doc/*/*md"

echo "Files: " $FILES
echo "Exclude: " $EXCLUDE

cd ../$DIST
rm $NAME-$OS-$VER.zip
zip -r $NAME-$OS-$VER.zip $FILES $EXCLUDE

