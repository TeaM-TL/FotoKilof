**Tomasz Łuczak**

# FotoKilof

---

[TOC]

---

## Wprowadzenie
Sympatyczny interfejs graficzny dla podstawowych poleceń programu ImageMagick dla przetwarzania obrazków.

### Konwersje
 - skalowanie z zachowaniem proporcji,
 - wycinek - trzy metody zaznaczania obszaru,
 - dodanie tekstu do obrazka, wewnątrz i na zewnątrz (generator memów),
 - ramka wokół obrazka,
 - obrót,
 - czarno-biały albo sepia,
 - zmiana kontrastu, normalizacja i rozciąganie kontrastu,
 - normalizacja koloru: auto-level lub wyrównanie histogramu,
 - odbicie lustrzane: w poziomie i w pionie,
 - dodanie własnego logo do obrazka.

### Funkcje
 - przetwarzanie obrazków w formatach JPG, PNG, SVG i TIF,
 - konwersja obrazków do formatu JPG, PNG i TIF,
 - przetwarzanie tylko kopii obrazków, oryginały są bezpieczne,
 - przetwarzanie jednego pliku jak i całego katalogu,
 - wykonywanie zrzutu ekranu (Linux) lub pobieranie ze schowka (Windows, MacOS)
 - wyświetlanie tylko aktywnych narzędzi,
 - wybór narzędzi przetwarzania,
 - podgląd oryginału i wyniku przetwarzania,
 - skalowanie własne (w pikselach lub procentach) lub predefiniowane: FullHD, 2k, 4k,
 - zaznaczania wycinka przez zaznaczenie na podglądzie lub za pomocą współrzędnych,
 - współrzędne wycinka można podać jako:
     - współrzędne dwóch przeciwległych narożników (lewy-góry i prawy-dolny),
     - współrzędne lewego-górnego narożnika oraz szerokości i wysokości wycinka,
     - szerokość i wysokość wycinka, grawitacja i odsunięcie od kierunku grawitacji,
 - wybór koloru, fontu i wielkości dodawanego tekstu oraz pozycji (bezwzględne lub grawitacja),
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
 - szybka nawigacja klawiszami `<Home>`, `<End>`, `<PgUp>`, `<PgDn>`

### Zrzuty ekranu

#### Linux
![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof1.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof2.png)

#### Mac OSX
![Screenshot MacOS](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_macos.png)

#### Windows
![Screenshot Windows](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_windows.png)

---

## Jak używać

### Podstawowe operacje
 - Wybierz plik obrazka, niezależnie czy chcesz przetwarzać pojedynczy plik czy cały katalog.
 - Przyciski *Poprzedni*, *Następny*, *Pierwszy* i *Ostatni* (lub klawisze `<PgUp>`, ` <PgDn>`, `<Home>`, `<End>`) nawigują pomiędzy obrazkami w bieżącym katalogu.
 - Przyciski *Podgląd* otwierają obrazek w domyślnej przeglądarce.

### Przetwarzanie pojedynczego polecenia
 - Zaznacz typ konwersji w panelu *Narzędzia*, np. *Obrót*.
 - W widgecie *Obrót* wybierz kąt, np. *90*.
 - Kliknij *Wykonaj*.

### Przetwarzanie wielu poleceń
 - Zaznacz typy konwersji w panelu *Narzędzia*, np. *Obrót*, *Ramka*.
 - W widgecie *Obrót* wybierz kąt, np. *180*,
 - w widgecie *Ramka* wybierz ulubiony kolor za pomocą przycisku *Kolor* i wpisz szerokość ramki np.*25*.
 - Kliknij *Wykonaj wszystko*.

### Przetwarzanie wszystkich plików w katalogu
 - Wybierz jeden z plików w katalogu.
 - Poćwicz na nim konwersje, jak w punkcie powyżej.
 - Zaznacz *Folder*, a następnie,
 - kliknij *Wykonaj wszystko*.

### Zrzuty ekranu

#### Linux
- Wybierz przycisk *Zrzut ekranu*.
- Kliknij w okno, którego obraz chcesz przechwycić.
- Można zmiast kliknięcia, kliknąć i przytrzymać lewy klawsz myszy, by zaznaczyć obszar.

#### Windows, MacOS
- Obraz pobierany jest ze schowka (może to być zrzut lub skopiowany obraz),
- Kliknij *Schowek*, by pobrać obraz ze schowka

#### Wspólne
- Obraz pojawi się w oknie podglądu FotoKilofa.
- Zrzut ekranu jest automatycznie zapisywany w katalogu *$TMP/%Y-%m-%D*, np. /tmp/2020-12-26.
- Po przetworzeniu obraz wynikowy zapisywany jest w podkatalogu *FotoKilof*.

### Konfiguracja
 - Przycisk *Zapisz* zapisuje bieżące ustawienia do pliku konfiguracyjnego *~/.fotokilof.ini*.
 - Przycisk *Wczytaj* odczytuje ustawienia z pliku konfiguracyjnego *~/.fotokilof.ini*.
 - Po zapisaniu konfiguracji, przy ponownym otwarciu, program odczyta konfigurację.

---

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
Można także podać bezwzględną pozycję tekstu na obrazku (np. wskazując lewym przyciskiem myszy).

Ponadto można wybrać font, wielkość i kolor tekstu. Można także po zaznaczeniu haczyka *Tło* wybrać kolor tła.

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

---

## Instalacja

### Jako pakiet pypi

```
python3 -m pip install --upgrade fotokilof
```

### Wymagania

 - Ekran FullHD dla komfortowej pracy
 - ImageMagick: https://imagemagick.org/ lub GraphicsMagick
 - Windows, Linux, MacOS X, BSD

#### Uruchomienie
`fotokilof`

---

## Podziękowania

 - Przyjaciołom - za inspirację, rady i testowanie,
 - Max von Forell - niemieckie tłumaczenie GUI,
 - Bozhidar Kirev - bułgarskie tłumaczenie GUI,
 - Afif Hendrawan - indonezyjskie tłumaczenie GUI
 - Alexander Ignatov - bułgarskie tłumaczenie GUI,
 - Sebastian Hiebl - poprawne pakowanie,
 - Matt Sephton - pomysł na pakowanie gui,
 - emsspree - aktualizacja niemieckiego tłumaczenia, jpeg,
 - Olm - testowanie pod Windows.

---

## Licencja

MIT License

Copyright (c) 2019-2021 Tomasz Łuczak, TeaM-TL

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

