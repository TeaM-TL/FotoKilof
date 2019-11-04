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
 - normalizacja koloru/auto-level/wyrównanie histogramu
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
 - wybór koloru, fontu i wielkości dodawanego tekstu,
 - szybka nawigacja po plikach przeyciskami: *Pierwszy*, *Następny*, *Poprzedni*, *Ostatni*
 - wyświetlanie histogramu iryginału i wyniku przetwarzania,
 - Edytor własnych poleceń. Polecenia mogą być składane z wykonywanych przetwarzań.

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
Skalowanie polega na takim przeskalowaniu obrazka, by zmieścił się w zadanych wymiarach, bez zniekształceń.
Do wyboru mamy trzy predefiniowane wymiary: FullHD (1920x1050), 2K (2058x1556) i 4K (4096x2112). Ponadto można podać maksymalny rozmiar w pikselach lub w procentach (odnosi się do rozmiaru pierwowzoru).

### Wycinek
Możemy wyciąć z obrazka interesujący nas fragment. Wycięcia możemy dokonać na trzy sposoby:
- przez podanie współrzędnych lewego górnego i prawego dolnego narożnika obrazka,
- przez podanie współrzędnych lewego górnego narożnika oraz wymiarów obrazka,
- przez podanie przesunięcia względem wybranej grawitacji oraz wymiarów obrazka. Grawitację wybieramy przyciskami oznaczającymi strony świata (np. N - północ, E - wschód itd), czyli kierunki do których wycinek będzie *ciążyć*.

Należy pamiętać, że współrzędne lewego górnego narożnika to (0,0).

Przycisk *Podgląd* rysuje żółtym kolorem obrys obszaru do wycięcia. Po każdej zmianie współrzędnych należy go przycisnąć by zaktualizować podgląd.

Dla ułatwienia wyboru pierwszego wariantu można zaznaczyć na podglądzie obszar do wycięcia: klikając lewym przyciskiem myszy na podglądzie oryginału wskazujemy lewy górny narożnik prostokąta do wycięcia, a prawym klawiszem myszy wskazujemy prawy dolny narożnik. Zaznaczone współrzędne wpisywane są do odpowiednich pól, które możemy jeszcze skorygować.

Ponadto przycisk *Z obrazka* odczytuje rozmiar obrazka i wpisuje je do odpowiednich pól.

### Tekst

Możemy dodać własny tekst do obrazka, np. podpis czy komentarz.

Tekst umieszczany jest *grawitacyjnie* na obrazku, czyli wybieramy kierunek ciążenia (W - zachód, S - południe itd.) oraz przesunięcie względem kierunku ciążenia.

Ponadto można wybrać font (niekoniecznie pod Windows), wielkość i kolor tekstu. Można także po zaznaczeniu haczyka *Tło* wybrać kolor tła.

### Obrót

Mamy predefiniowane trzy kąty obrotu obrazka: 90, 180 i 270 stopni.

Gdybyśmy chcieli iny kąt obrotu niż predefiniowane, to po kliknięciu na przycisk *Obrót*, w polu *Własne* zostanie wpisane polecenie obrotu. Można wówczas zmienić kąt obrotu na inny.

### Ramka

Obrazek można oprawić w ramkę o zadanej grubości i kolorze.

### Czarno-białe

Obrazek możemy skonwertować do sepii (domyślna wartość to 95%) lub do obrazka czarno-białego.

### Normalizacja kolorów

Mamy trzy narzędzia do normalizacji kolorów:
- wyrównanie (Equalize), można dodatkowo wybrać kanał (domyślnie *None*)
- normalizacja
- autoLevel - automatyczne wyrównanie poziomów

### Kontrast

Możemy zmienić kontrast obrazka w zakresie do -3 do +3, skokowo co 1.

Drugą możliwością jest rozciągnięcie kontrastu od czerni do bieli. Domyślne wartości to 0,15 (czerń) i 0,05 (biel)

### Histogram

Jeśli chcemy, to program może wygenerować i wyświetlić histogramy obrazka pierwotnego i wynikowego, po konwersji.

### Własne konwersje

Wszystkie uruchamiane polecenia przetwarzania wpisywane są do pola *Własne polecenia*, gdzie możemy skomponować własny przepis przetwarzania obrazka. Np. podać inny niż predefiniowany kąt obrotu, czy ujemne przesunięcia dla grawitacji.
Znając polecenia przetwarzania programu *ImageMagick* można w tym polu wpisywać te polecenia. Jeśli nastąpi błąd, to w oknie komunikatów, może zostać wyświetlony odpowiedni komunikat.

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
* rozpakuj i uruchom ()

### Wymagania

 - Ekran FullHD dla komfortowej pracy
 - ImageMagick: https://imagemagick.org/ lub GraphicsMagick
 - Windows, Linux, MacOS X, BSD

### Ze źródeł
Tylko gdy uruchamiamy ze źródeł

#### Python3 i moduły

#### via pip
 - configparser,
 - datetime,
 - pathlib,
 - Pillow (zawiera tkcolorpicker),
 - touch,

### via pakiety
 - tkinter,

#### powinny być w zestawie
 - gettext,
 - glob,
 - os,
 - platform,
 - re,
 - shutil.

#### Uruchomienie
`python3 fotokilof.py`

## Podziękowania

 - Przyjaciołom - za inspirację i rady,
 - Max von Forell - niemieckie tłumaczenie GUI
 - Bozhidar Kirev - bułgarskie tłumaczenie GUI
 - Afif Hendrawan - indonezyjskie tłumaczenie GUI

## Licencja

MIT License

Copyright (c) 2019 Tomasz Łuczak, TeaM-TL

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

