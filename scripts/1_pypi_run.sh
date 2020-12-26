#!/usr/bin/env bash
VERSION=`cat ../src/__VERSION__`
python3 ../dist/FotoKilof-$VERSION-py3-none-any.whl/src &
exit
