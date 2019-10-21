#!/bin/sh
DIST=dist
OUT=locale.zip
DOC=doc/*/*pdf
LOCALES=locale/*/*/fotokilof.mo
LICENSE=LICENSE

cd ../$DIST
zip $OUT $LICENSE $LOCALES $DOC
cd ..

