#!/usr/bin/env bash

CWD=`pwd`
INITPY="src/__init__.py"
MAINPY="src/fotokilof.py"
MAIN__PY="src/__main__.py"

echo "- PyPI ---"

cd ..
touch $INITPY
mv $MAINPY $MAIN__PY

# Python 3.8
#python3 setup.py sdist bdist
# Python 3.7
python3 setup.py sdist bdist_wheel

mv $MAIN__PY $MAINPY
cd $CWD

# EOF

