#!/bin/sh
DIST=dist
OUT=$DIST/fotokilof.zip 
DOC=$DIST/doc/*/*pdf
LOCALES=$DIST/locale/*/*/fotokilof.mo
LICENSE=$DIST/LICENSE*
EXE=$DIST/*.exe
XML=$DIST/*.xml

cd ..
zip $OUT $EXE $XML $LICENSE $LOCALES $DOC

