#!/usr/bin/env bash

CWD=`pwd`
INITPY="fotokilof/__init__.py"
MAINPY="fotokilof/fotokilof.py"
MAIN__PY="fotokilof/__main__.py"

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

