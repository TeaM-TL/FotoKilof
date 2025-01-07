#!/usr/bin/env bash

rm -rf ../build/*
rm -rf ../fotokilof/__pycache__
CWD=`pwd`



cd ..
echo "- Locale ---"
LC_LAST=LC_MESSAGES/fotokilof
for L in fotokilof/locale/??; do
    if [ -e $L/$LC_LAST.po ]; then
        msgfmt $L/$LC_LAST.po -o $L/$LC_LAST.mo
        ls $L/$LC_LAST*
    fi
done

echo "- PyPI ---"
python -m build --wheel
cd $CWD

echo "for testing only, package is build by GitHub actions and publish in PyPi automatically"

# EOF
