#!/bin/sh
# $Id: 0_pyinstaler 9 2019-08-30 14:28:33Z tlu $
rm -rf __pycache__ build
#pyinstaller --onefile --windowed fotokilof.py
pyinstaller --onefile src/fotokilof.py
rm -rf build

