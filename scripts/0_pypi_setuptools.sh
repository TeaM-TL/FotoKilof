#!/usr/bin/env bash

CWD=`pwd`
INITPY="src/__init__.py"

echo "- PyPI ---"

cd ..
touch $INITPY
python3 setup.py bdist_wheel

rm $INITPY
cd $CWD

# EOF

