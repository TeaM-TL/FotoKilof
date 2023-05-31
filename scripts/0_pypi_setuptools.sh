#!/usr/bin/env bash

rm -rf ../build/*
rm -rf ../fotokilof/__pycache__
CWD=`pwd`

echo "- PyPI ---"

cd ..

# Python 3.8
#python3 setup.py sdist bdist
# Python 3.7
python3 setup.py sdist bdist_wheel

cd $CWD

# EOF

