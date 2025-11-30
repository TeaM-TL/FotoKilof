#!/bin/bash

sudo apt-get install python3-requirement-parser python3-certifi flatpak-builder

#python3 -m pip install --user requirements-parser
#python3 -m pip install --upgrade certifi
export SSL_CERT_FILE=$(python3 -m certifi)

curl -O https://raw.githubusercontent.com/flatpak/flatpak-builder-tools/master/pip/flatpak-pip-generator.py
chmod +x flatpak-pip-generator.py

sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
sudo flatpak update
sudo flatpak install -y flathub org.freedesktop.Sdk//25.08
sudo flatpak install -y flathub org.freedesktop.Platform//25.08

# python3 flatpak-pip-generator.py \
#     --requirements-file=../requirements.txt \
#     --output=pypi-dependencies.json

sudo flatpak-builder --force-clean build-dir ../manifest.yml

