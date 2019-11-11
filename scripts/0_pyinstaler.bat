@REM $Id: 0_pyinstaler 9 2019-08-30 14:28:33Z tlu $
@ECHO OFF
cd ..
rmdir build /S /Q
rmdir src/__pycache__
SET UPX=--upx-dir upx
SET UPX=--noupx
SET ONEFILE=--onefile
SET ONEFILE=
pyinstaller --clean --console %ONEFILE% %UPX% src\fotokilof.py
pause
