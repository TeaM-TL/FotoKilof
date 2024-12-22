#!/usr/bin/env bash
echo "package test"
VERSION=`cat ../fotokilof/version.py | grep version | awk '{print $3}' | tr -d '"'`
python3 ../dist/FotoKilof-$VERSION-py3-none-any.whl/fotokilof &
exit
