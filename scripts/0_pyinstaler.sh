#!/bin/sh
# $Id: 0_pyinstaler 9 2019-08-30 14:28:33Z tlu $
cd ..
rm -rf __pycache__ build
#pyinstaller --onefile --windowed fotokilof.py
UPX="--upx-dir=upx"
UPX=
pyinstaller --clean --onefile $UPX src/fotokilof.py
rm -rf build

