#!/bin/sh
VER=`cat ../src/version.py | grep "__version__" | cut -f3 -d ' '| sed 's/"//g'`
echo "FotoKilof-$VER"
python3 -m twine upload ../dist/FotoKilof-$VER*

#EOF

