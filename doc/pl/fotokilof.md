**Tomasz Łuczak**

# FotoKilof

------
[TOC]

## Wprowadzenie
Sympatyczny interfejs graficzny dla podstawowych poleceń programu ImageMagick dla przetwarzania obrazków. Umożliwia użycie innych poleceń programów *convert*, *mogrify* i *compose*.

### Konwersje
 - skalowanie z zachowaniem proporcji,
 - wycinek - trzy metody zaznaczania obszaru,
 - dodanie tekstu do obrazka, wewnątrz i na zewnątrz (generator memów)
 - ramka wokół obrazka,
 - obrót,
 - czarno-biały albo sepia,
 - zmiana kontrastu, normalizacja i rozciąganie kontrastu,
 - normalizacja koloru: auto-level lub wyrównanie histogramu
 - dodanie własnego logo do obrazka.

### Funkcje
 - przetwarzanie obrazków w formatach JPG, PNG, SVG i TIF,
 - konwersja obrazków do formatu JPG, PNG i TIF,
 - przetwarzanie tylko kopii obrazków, oryginały są bezpieczne,
 - przetwarzanie jednego pliku jak i całego katalogu,
 - wykonywanie zrzutu ekranu,
 - wyświetlanie tylko aktywnych narzędzi,
 - wybór narzędzi przetwarzania,
 - podgląd oryginału i wyniku przetwarzania,
 - skalowanie własne (w pikselach lub procentach) lub predefiniowane: FullHD, 2k, 4k,
 - zaznaczania wycinka przez zaznaczenie na podglądzie lub za pomocą współrzędnych,
 - współrzędne wycinka można podać jako:
     - współrzędne dwóch przeciwległych narożników (lewy-góry i prawy-dolny),
     - współrzędne lewego-górnego narożnika oraz szerokości i wysokości wycinka,
     - szerokość i wysokość wycinka, grawitacja i odsunięcie od kierunku grawitacji,
 - wybór koloru, fontu i wielkości dodawanego tekstu,
 - predefiniowane kąty obrotu: 90, 180 i 270 lub własne,
 - regulowana sepia,
 - wyrównanie (*Equalize*) także dla pojedynczego kanału,
 - kontrast regulowany w zakresie od -3 do +3,
 - rozszerzanie kontrastu,
 - wyświetlanie histogramu oryginału i wyniku przetwarzania,
 - szybka nawigacja po plikach przyciskami: *Pierwszy*, *Następny*, *Poprzedni*, *Ostatni*,
 - edytor własnych poleceń,
 - polecenia mogą być składane z wykonywanych przetwarzań,
 - można korzystać z innych poleceń ImageMagick np. *-gaussian-blur*,
 - logowanie konwersji i komunikatów wewnętrznych,
 - częściowe wsparcie dla GraphicsMagick.

### Zrzuty ekranu

#### Linux
![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof1.png)

#### Mac OSX
![Screenshot MacOS](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_macos.png)

#### Windows
![Screenshot Windows](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_windows.png)

## Jak używać

### Podstawowe operacje
 - Wybierz plik obrazka, niezależnie czy chcesz przetwarzać pojedynczy plik czy cały katalog.
 - Przyciski *Poprzedni* i *Następny* otwierają kolejny lub poprzedni obrazek w katalogu.
 - Przyciski *Pierwszy* i *Ostatni* otwierają pierwszy lub ostatni obrazek w katalogu.
 - Przycisk *Zapisz* zapisuje bieżące ustawienia do pliku konfiguracyjnego *.fotokilof.ini*.
 - Przycisk *Wczytaj* odczytuje ustawienia z pliku konfiguracyjnego *.fotokilof.ini*.
 - Plik konfiguracyjny *.fotokilof.ini* zapisywany jest w katalogu użytkownika.
 - Po zapisaniu konfiguracji, przy ponownym otwarciu, program odczyta konfigurację.
 - Przyciski *Podgląd* otwierają obrazek w domyślnej przeglądarce.
 - Program zamykamy poleceniem *Alt-F4* lub ikoną.

### Zrzuty ekranu

- Wybierz przycisk *Zrzut ekranu*.
- Kliknij w okno, którego obraz chcesz przechwycić.
- Można zmiast kliknięcia, kliknąć i przytrzymać lewy klawsz myszy, by zaznaczyć obszar.
- Obraz pojawi się w oknie podglądu FotoKilofa.
- Zrzut ekranu jest automatycznie zapisywany w katalogu *$TMP/%Y-%m-%D*, np. /tmp/2020-12-26.
- Po przetworzeniu obraz wynikowy zapisywany jest w podkatalogu *FotoKilof*.

### Przetwarzanie pojedynczego polecenia
 - Zaznacz typ konwersji w panelu *Narzędzia*, np. *Obrót*.
 - Kliknij *Zapisz*.
 - W widgecie *Obrót* wybierz kąt, np. *90*.
 - Kliknij *Wykonaj*.
 - Zobacz podgląd.

### Przetwarzanie wielu poleceń
 - Zaznacz typy konwersji w panelu *Narzędzia*, np. *Obrót*, *Ramka*.
 - Kliknij *Zapisz*.
 - W widgecie *Obrót* wybierz kąt, np. *180*, a widgecie *Ramka* wybierz ulubiony kolor za pomocą przycisku *Kolor* i wpisz szerokość ramki np.*25*.
 - Kliknij *Wykonaj wszystko*.
 - Zobacz podgląd.

### Przetwarzanie wszystkich plików w katalogu
 - Wybierz jeden z plików w katalogu.
 - Poćwicz na nim konwersje, jak w punkcie powyżej.
 - Zaznacz *Folder*, a następnie,
 - kliknij *Wykonaj wszystko*.
 - W oknie podglądu zostanie wyświetlony podgląd ostatniego z przetwarzanych obrazków.
 - Pod paskiem postępu zostanie wyświetlony numer pliku i jego nazwa oraz liczba wszystkich plików, które będą przetwarzane.

## Przetwarzania obrazu

### Skalowanie

Skalowanie polega na takim przeskalowaniu obrazka, by zmieścił się w zadanych wymiarach, bez zniekształceń czyli z zachowaniem proporcji.
Do wyboru mamy trzy predefiniowane wymiary: FullHD (1920x1050), 2K (2058x1556) i 4K (4096x2112). Ponadto można podać maksymalny rozmiar w pikselach lub w procentach (odnosi się do rozmiaru pierwowzoru).

### Wycinek
Możemy wyciąć z obrazka interesujący nas fragment. 

Wycięcia możemy dokonać na trzy sposoby:
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

Gdybyśmy chcieli podać inny kąt obrotu niż predefiniowane, to po kliknięciu na przycisk *Obrót*, w polu *Własne* zostanie wpisane polecenie obrotu. Można wówczas zmienić kąt obrotu na inny.

### Ramka

Obrazek można oprawić w ramkę o zadanej grubości i kolorze.

### Czarno-białe

#### Czarno-biały
Konwersja do skali szarości

#### Sepia

Symulacja tonów sepii. Można regulować próg intensywności (od 0 do 99,9%), domyślna wartość to 95%). Dokumentacja programu *ImageMagick* podaje że 80% jest dobrym punktem startu.

### Normalizacja kolorów

Narzędzia do normalizacji kolorów:

#### AutoLevel
Automagiczne wyrównanie poziomów kolorów obrazka.

#### Wyrównanie (Equalize)
Wyrównanie histogramu obrazka kanał po kanale. Można wybrać kanał (domyślnie *None*).

### Kontrast

##### Kontrast
Możemy zwiększać lub redukować kontrast obrazka w zakresie do -3 do +3, skokowo co 1.

##### Rozciągnięcie kontrastu

Drugą możliwością jest rozciągnięcie kontrastu od czerni do bieli. Domyślne wartości to 0,15 (czerń) i 0,05 (biel)

#### Normalizacja kontrastu
Zwiększenie kontrastu za pomocą rozciągnięcia zakresu intensywności.

### Histogram

Jeśli chcemy, to program może wygenerować i wyświetlić histogramy obrazka pierwotnego i wynikowego, po konwersji.

### Własne konwersje

Wszystkie uruchamiane polecenia przetwarzania wpisywane są do pola *Własne polecenia*, gdzie możemy skomponować własny przepis przetwarzania obrazka. Np. podać inny niż predefiniowany kąt obrotu, czy ujemne przesunięcia dla grawitacji.
Znając polecenia przetwarzania programu *ImageMagick* można w tym polu wpisywać te polecenia. Jeśli nastąpi błąd, to w oknie komunikatów, może zostać wyświetlony odpowiedni komunikat.

### Jeden plik albo cały katalog

W zależności od wyboru *Plik* albo *Folder*, przetwarzany będzie albo wybrany plik albo cały folder z wybranym plikiem.
Do przetwarzania folderu musimy użyć przycisku *Zaaplikuj wszystko* i zaznaczyć przycisk *Folder*.

## Instalacja

### Jako pakiet pypi

```
python3 -m pip install fotokilof
fotokilof
```

### Z paczki zip

- Rozpakuj plik *fotokilof.zip* do folderu, 
- zrób skrót na pulpicie,
- i uruchom.
> Windows: W przyszłości będzie dostępny instalator, wygenerowany za pomocą NSIS.

### Wymagania

 - Ekran FullHD dla komfortowej pracy
 - ImageMagick: https://imagemagick.org/ lub GraphicsMagick
 - Windows, Linux, MacOS X, BSD

### Ze źródeł
Tylko gdy uruchamiamy ze źródeł

Python3 i moduły:
 - via pip:
    - configparser,
    - tkcolorpicker (nieobligatoryjny, wymaga PIL),
    - PIL dla Windows do obsugi schowka,
 - via pakiety:
     - tkinter,
 - powinny być w zestawie:
     - datetime,
     - fnmatch,
     - gettext,
     - glob,
     - os,
     - platform,
     - re,
     - shutil,
     - tempfile.

#### Uruchomienie
`python3 fotokilof.py`

## Podziękowania

 - Przyjaciołom - za inspirację, rady i testowanie,
 - Max von Forell - niemieckie tłumaczenie GUI,
 - Bozhidar Kirev - bułgarskie tłumaczenie GUI,
 - Afif Hendrawan - indonezyjskie tłumaczenie GUI
 - Alexander Ignatov - bułgarskie tłumaczenie GUI,
 - Sebastian Hiebl - python packaging.


## Licencja

MIT License

Copyright (c) 2019-2020 Tomasz Łuczak, TeaM-TL

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
