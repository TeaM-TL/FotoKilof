#!/usr/bin/env bash

CWD=`pwd`
INITPY="src/__init__.py"
MAINPY="src/fotokilof.py"
MAIN__PY="src/__main__.py"

echo "- PyPI ---"

cd ..
touch $INITPY
mv $MAINPY $MAIN__PY

python3 setup.py bdist_wheel

mv $MAIN__PY $MAINPY
rm $INITPY
cd $CWD

# EOF

