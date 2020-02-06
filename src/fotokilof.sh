#!/bin/sh

# MYPATH - path to FotoKilof python source
MAIN=fotokilof.py
MYPATH="${0%/*}"
cd $MYPATH
python3 $MAIN &

