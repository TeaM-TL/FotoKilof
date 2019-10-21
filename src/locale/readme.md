## Translations

If there are not *fotokilof* in your language, you are able to do it. Example steps for Hungarian:
`NEWLANG=hu/LC_MESSAGES`
`mkdir -p $NEWLANG`
`cp fotokilof.pot $NEWLANG/fotokilof.po`
`cd $NEWLANG`
`vim fotokilof.po`
`msgfmt -o fotokilof.mo fotokilof`

### Advices

- add your name into *Last-Translator:* field

- to check changes from sources, change entry like this:

`"X-Poedit-Basepath: ../../\n"`

## Test

`cd ../../../`
`python3 fotokilof.py`