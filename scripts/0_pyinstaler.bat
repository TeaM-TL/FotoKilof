@ECHO OFF
cd ..
rmdir build /S /Q
rmdir fotokilof\__pycache__ /S /Q
SET UPX=--upx-dir upx
SET UPX=--noupx
SET ONEFILE=--onefile
SET ONEFILE=
pyinstaller --noconfirm --clean --console %ONEFILE% %UPX% fotokilof\fotokilof.py
pause
cd scripts
