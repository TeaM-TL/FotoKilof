#!/usr/bin/env bash

rm -rf ../build/*
rm -rf ../fotokilof/__pycache__
CWD=`pwd`

echo "- PyPI ---"

cd ..

# deprecated
# python3 setup.py sdist bdist_wheel
# current, require package build
python -m build --wheel
cd $CWD

# EOF

