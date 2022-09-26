#!/usr/bin/env bash
VERSION=`cat ../src/version.py | grep version | awk '{print $3}' | tr -d '"'`
python3 ../dist/FotoKilof-$VERSION-py3-none-any.whl/src &
exit
