#!/bin/bash
echo "refresh pot file"

cd ../fotokilof
xgettext -d fotokilof -o locale/fotokilof.pot *py
