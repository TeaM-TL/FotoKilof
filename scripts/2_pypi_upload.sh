#!/bin/sh
VERSION=`cat ../src/version.py | grep version | awk '{print $3}' | tr -d '"'`
echo "FotoKilof-$VERSION"
python3 -m twine upload ../dist/FotoKilof-$VERSION*

#EOF

