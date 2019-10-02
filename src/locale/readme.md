## Translate fotokilof in four steps:
### steps:
cp fotokilof.pot hu/LC_MESSAGES/fotokilof.po

cd hu/LC_MESSAGES

vim fotokilof.po

msgfmt -o fotokilof.mo fotokilof

### test it:
cd ../../../

python3 fotokilof.py
