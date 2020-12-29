@ECHO OFF
cd ..
rmdir build /S /Q
rmdir src\__pycache__/S /Q
SET UPX=--upx-dir upx
SET UPX=--noupx
SET ONEFILE=--onefile
SET ONEFILE=
pyinstaller --noconfirm --clean --console %ONEFILE% %UPX% src\fotokilof.py
pause
cd scripts
