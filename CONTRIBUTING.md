## Localization

### Preparing
NEWLANG=hu/LC_MESSAGES

mkdir -p $NEWLANG

cp fotokilof.pot $NEWLANG/fotokilof.po

cd $NEWLANG

### Translation
[vim|emacs|poedit] fotokilof.po

Is good idea to yoyr name into LastTranslator field

msgfmt -o fotokilof.mo fotokilof

### Test
cd ../../../

python3 fotokilof.py

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

### n - number
numbering widgets with the same fuction

### B - frame
 name of frame, which contains this widget

### C - function
 function of widget, eg. run, show, etc.
 
### n - number

numbering widgets with the same fuction or 
numbering function

### I know
I have to implement this standard in my code :-)
