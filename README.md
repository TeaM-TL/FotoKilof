# FotoKilof - GUI for ImageMagick
GUI for the most used by me ImageMagick functionality for processing pictures

![Screenshot](https://github.com/TeaM-TL/FotoKilof/blob/master/screenshots/fotokilof.png)

![Screenshot](https://github.com/TeaM-TL/FotoKilof/blob/master/screenshots/fotokilof1.png)

![Screenshot](https://github.com/TeaM-TL/FotoKilof/blob/master/screenshots/fotokilof2.png)

## Graphics conversion
 - rotation (90, 180, 270 degree)
 - frame around picture
 - text annotation
 - black-white or sepia conversion
 - contrast or histogram stretching
 - color normalize/auto-level
 - crop (three ways selection)
 - scaling/resize: own size (in pixel or percent) or predefined: HD, 2k, 4k,
## Functionality:
 - processing copy of picture, originals are safe
 - processing single file or whole directory,
 - display selected tools,
 - tools selection
 - preview
 - crop selection via click on preview or coordinates, in three ways
 - text: color, font and size selection (Linux, Mac OSX only)
 - fast file navigation: First, Prev, Next, Last
 - histograms of original and result pictures.

## Requirements
 - ImageMagick - home page: https://imagemagick.org/
 - Windows, Linux, MacOS X, BSD
 - FullHD screen for comfort work
 - Python3, with modules: PIL, tkinter, tkcolorpicker - only for script launch

## Using
### source code
python fotokilof.py
### binary
fotokilof
### translations
mkdir -p pl/LC_MESSAGES; cp pl.mo pl/LC_MESSAGES/fotokilof.mo

### Binaries
In Release you can find current binary version for Windows (8.1 and newer) and Linux (Ubuntu 18.04.3 and newer)

## Users Guide
1. Wybierz plik
2. Przyciski Poprzedni i Następny otwierają kolejny lub poprzedni obrazek
3. Klikając lewm przyciskiem myszy na podglądzie oryginału wskazujemy
lewy górny narożnik prostokąta do wycięcia, a prawym klawiszem myszy
wskazujemy prawy dolny narożnik, ważne by zaznaczyć Współrzędne (x1,y1)(x2,y2).
Klikając powtórnie na wyborzy typu wycinka na podglądzie oryginału 
zostaną narysowane linie cięcia, względem wybranych punktów.
4. W zależności od wyboru Plik albo Folder, przetwarzany będzie albo 
wybrany plik albo cały folder z wybranym plikiem.
Do przetwarzania folderu musimy użyć przycisku Zaaplikuj wszystko i zaznaczyć przycisk folder
5. Wybór Nic, 0 szerokości ramki i odhaczenie Tekst, wyłącza dane 
polecenie z przetwarzania


