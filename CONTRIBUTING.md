## Localization

If there are not *fotokilof* in your language, you are able to do it. Example steps for Hungarian:

```
cd src/locale
NEWLANG=hu/LC_MESSAGES
mkdir -p $NEWLANG
cp fotokilof.pot $NEWLANG/fotokilof.po
cd $NEWLANG
[vim|poedit] fotokilof.po
msgfmt -o fotokilof.mo fotokilof
```

### Advices

- add your name into *Last-Translator:* field

- to check changes from sources, change entry like this:

`"X-Poedit-Basepath: ../../\n"`

### Test

```
cd ../../../
python3 fotokilof.py
```

---

## Widgets naming:
 *An_B_Cn*

### A - widget type:
 - b - button
 - rb - radiobutton
 - cb - checkbutton
 - co - combobox
 - e - entry
 - l - label
 - lb - listbox
 - t - text
 - pb - progressbar
 - pi - PhotoImage
 - f, frame - frame or labelframe

### n - number
numbering widgets with the same fuction

### B - frame
 name of frame, which contains this widget

### C - function
 function of widget, eg. run, show, etc.

### n - number

numbering widgets with the same fuction or 
numbering function
