#!/bin/bash

python3 -m pip install --user requirements-parser
python3 -m pip install --upgrade certifi
export SSL_CERT_FILE=$(python3 -m certifi)

curl -O https://raw.githubusercontent.com/flatpak/flatpak-builder-tools/master/pip/flatpak-pip-generator.py
chmod +x flatpak-pip-generator.py

flatpak-builder --force-clean build-dir ../manifest.yml

python3 flatpak-pip-generator.py --requirements-file=../requirements.txt --output=pypi-dependencies.json