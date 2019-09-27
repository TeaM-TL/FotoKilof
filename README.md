# FotoKilof
Graficzny interface do ImageMagick

![Screenshot](https://github.com/TeaM-TL/FotoKilof/blob/master/screenshots/fotokilof.png)

![Screenshot](https://github.com/TeaM-TL/FotoKilof/blob/master/screenshots/fotokilof1.png)

![Screenshot](https://github.com/TeaM-TL/FotoKilof/blob/master/screenshots/fotokilof2.png)

## Funkcje:
 - przetwarzanie pojedynczego pliku jak i całego katalogu,
 - wybór wyświetlanych narzędzi
 - obrót co 90stopni
 - wycinanie: własne i predefiniowane wielkości (HD, 2K, 4K),
 - klikany podgląd, wczytuje współrzędne do wycinka, podgląd wybranego wycinka
 - dodawanie tekstu i koloru tła
 - wybór fontu (Linux, Mac OSX) i koloru
 - normalizacja kolorów,
 - dodawanie ramki, wybór szerokości i koloru
 - czarno-białe, sepia (regulowana),
 - zmiana kontrastu (4 nastawy) i rozciaganie histogramu,
 - szybka nawigacja po katalogu przyciskami: Następny, Poprzedni
 - podgląd oryginału i wyniku,
 - histogram oryginału i wyniku,

## Wymagania
 - ImageMagick - zainstaluj stąd: https://imagemagick.org/
 - Windows, Linux, MacOS X, BSD
 - Ekran FullHD
 - Python3, z modułami: PIL, tkinter, tkcolorpicker - tylko do uruchomienia źródła skryptu

## Uruchomienie
### Ze źródła
python fotokilof.py

### Binaria
W karcie Releases znajdują się aktualne binaria dla Windows (8.1 i nowsze)
i Linuksa (Ubuntu 18.04.3 i nowsze)

## Instrukcja
1. Wybierz plik
2. Przyciski Poprzedni i Następny otwierają kolejny lub poprzedni obrazek
3. Klikając lewm przyciskiem myszy na podglądzie oryginału wskazujemy
lewy górny narożnik prostokąta do wycięcia, a prawym klawiszem myszy
wskazujemy prawy dolny narożnik, ważne by zaznaczyć Współrzędne (x1,y1)(x2,y2).
Klikając powtórnie na wyborzy typu wycinka na podglądzie oryginału 
zostaną narysowane linie cięcia, względem wybranych punktów.
4. W zależności od wyboru Plik albo Folder, przetwarzany będzie albo 
wybrany plik albo cały folder z wybranym plikiem.
Do przetwarzania folderu musimy użyć przycisku Zaaplikuj wszystko.
5. Wybór Nic, 0 szerokości ramki i odhaczenie Tekst, wyłącza dane 
polecenie z przetwarzania

## Do Zrobiena
1. Internalizacja
2. wersja obiektowa
3. PIL zamiast ImageMagick, o ile się da lub gdzie się da
4. Instalator NSIS dla Windows
5. Instrukcja obsługi, filmik, pl, en
6. paned window bo może wyjść poza ekran

