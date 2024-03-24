#!/bin/sh
VERSION=`cat ../fotokilof/version.py | grep version | awk '{print $3}' | tr -d '"'`
echo "FotoKilof-$VERSION"
python3.11 -m twine upload ../dist/FotoKilof-$VERSION*

#EOF

