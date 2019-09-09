# FotoKilof
Graficzny interface do ImageMagick

## Wymagania
1. ImageMagick - zainstaluj stąd: https://imagemagick.org/
2. Windows, Linux, MacOS
3. Ekran FullHD
4. Python3, z modułami: PIL, tkinter, tkcolorpicker

## Uruchomienie
### Ze źródła
python fotokilof.py

### Binaria
W katalogi dist znajdują się aktualne binaria dla Windows (8.1 i nowsze)
i Linuksa (Xubuntu 18.04.3 i nowsze)

## Instrukcja
1. Wybierz plik
2. Przyciski Poprzedni i Następny otwierają kolejny lub poprzedni obrazek
3. Klikając lewm przyciskiem myszy na podglądzie oryginału wskazujemy
lewy górny narożnik protokata do wycięcia, a prawym klawiszem myszy
wskazujemy prawy dolny narożnik, ważne by zaznaczyć Współrzędne (x1,y1)(x2,y2).
Klikając powtórnie na wyborzy typu wycinka na podglądzie oryginału 
zostaną narysowane linie cięcia, względem wybranych punktów.
4. W zależności od wyboru Plik albo Folder, przetwarzany będzie albo 
wybrany plik albo cały folder z wybranym plikiem.
Do przetwarzania folderu musimy użyć przycisku Zaaplikuj wszystko.
5. Wybór Nic, 0 szerokości ramki i odhczenie Tekst, wyłącza dane 
polecenie z przetwarzania
