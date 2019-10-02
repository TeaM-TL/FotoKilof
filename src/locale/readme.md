## Translate fotokilof in easy way steps:
### steps:
NEWLANG=hu/LC_MESSAGES

mkdir -p $NEWLANG

cp fotokilof.pot $NEWLANG/fotokilof.po

cd $NEWLANG

vim fotokilof.po

msgfmt -o fotokilof.mo fotokilof

### test it:
cd ../../../

python3 fotokilof.py
