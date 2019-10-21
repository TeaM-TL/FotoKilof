**Tomasz Łuczak**

# FotoKilof

------
[TOC]

## Wprowadzenie
Sympatyczny interfejs graficzny dla podstawowych poleceń programu ImageMagick dla przetwarzania obrazków.

### Konwersje

 - obrót (90, 180, 270 degree),
 - ramka wokół obrazka,
 - dodanie tekstu do obrazka,
 - czarno-biały albo sepia,
 - zmiana kontrastu i rozciąganie kontrastu,
 - normalizacja koloru/auto-level
 - wycinek - trzy metody zaznaczania obszaru,
 - skalowanie: włane (w pikselach lub procentach) lub predefiniowane: HD, 2k, 4k,
 - dodanie własnego logo do obrazka.

### Funkcje

 - przetwarzanie kopii obrazków, oryginały są bezpieczne,
 - przetwarzanie jednego pliku jak i całego katalogu,
 - wyświetlanie tylko aktywnych narzędzi,
 - wybór narzędzi przetwarzania,
 - podgląd oryginału i wyniku przetwarzania,
 - zaznaczania wycinka przez zaznaczenie na podglądzie lub za pomocą współrzędnych, trzema metodami,
 - wybór koloru, fontu i wielkościdodawanego tekstu,
 - szybka nawigacja po plikach przeyciskami: *Pierwszy*, *Następny*, *Poprzedni*, *Ostatni*
 - wyświetlanie histogramu iryginału i wyniku przetwarzania,
 - Edytor własnych polceń, polecenia mogą być składane z wykonywanych przetwarzań.

### Zrzuty ekranu

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof1.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof2.png)

## Jak użyć

 - Wybierz plik
 - Przyciski Poprzedni i Następny otwierają kolejny lub poprzedni obrazek
 - Wybierz typy konwersji
 - Kliknij na przycisku Wykonaj

### Skalowanie

### Wycinek

Klikając lewm przyciskiem myszy na podglądzie oryginału wskazujemy lewy górny narożnik prostokąta do wycięcia, a prawym klawiszem myszy wskazujemy prawy dolny narożnik, ważne by zaznaczyć Współrzędne (x1,y1)(x2,y2).

Klikając powtórnie na wyborzy typu wycinka na podglądzie oryginału zostaną narysowane linie cięcia, względem wybranych punktów.

### Tekst

### Obrót

### Ramka

### Czarno-białe

### Normalizacja kolorów

### Kontrast

### Histogram

### Własne konwersje

### Jeden plik albo cały katalog

W zależności od wyboru *Plik* albo *Folder*, przetwarzany będzie albo wybrany plik albo cały folder z wybranym plikiem.
Do przetwarzania folderu musimy użyć przycisku *Zaaplikuj wszystko* i zaznaczyć przycisk *Folder*.

## Instalacja

### Windows

- Rozpakuj plik *fotokilof.zip* do folderu, 
- zrób skrót na pulpicie,
- i uruchom.
> W przyszłości będzie dostępny instalator, wygenerowany za pomocą NSIS.

### Linux, MacOSX, *BSD
* rozpakuj i uruchom

### Wymagania

 - ImageMagick: https://imagemagick.org/ lub GraphicsMagick
 - Windows, Linux, MacOS X, BSD
 - Ekran FullHD dla komfortowej pracy

### Ze źródeł
Tylko gdy uruchamiamy ze źródeł

#### Python3 i moduły
 - configparser,
 - datetime,
 - gettext,
 - glob,
 - os,
 - platform,
 - PIL,
 - tkinter,
 - tkcolorpicker,
 - touch,
 - re,
 - shutil.

#### Uruchomienie
`python3 fotokilof.py`

## Podziękowania
 - Przyjaciołom - za inspirację i rady,
 - Max von Forell - niemieckie tłumaczenie GUI
 - Bozhidar Kirev - bułgarskie tłumaczenie GUI
 - Afif Hendrawan - indonezyjskie tłumaczenie GUI

