#!/bin/sh

# MYPATH - path to FotoKilof python source

MYPATH="${0%/*}"
cd $MYPATH
python3 __main__.py &

