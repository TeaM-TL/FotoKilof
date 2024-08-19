# FotoKilof - GUI for ImageMagick

GUI for the most used (by me) ImageMagick functionality for processing pictures.

## Screenshots

### Linux

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_linux.png)

### Linux dark mode

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_linux_dark.png)

### Windows

![Screenshot Windows](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_windows.png)

### macOS compose

![Screenshot Windows](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_compose.png)

## Graphics conversion

 - scaling/resize,
 - crop,
 - text annotation, inside or outside of picture (mems generator),
 - border around picture,
 - rotation,
 - mirroring (vertical or horizontal)
 - black-white
 - sepia - only with Wand and ImageMagick,
 - contrast increase/decrease or normalize or histogram stretching,
 - color auto-level or equalize,
 - vignette
 - adding logo image on picture,
 - compose two image in one picture
 - file formats: JPG, PNG, TIFF, SVG
 - format conversion into JPG, PNG, TIFF.

## Functionality:

 - processing JPG, PNG, SVG and TIFF images,
 - processing picture in the fly, originals are safe,
 - processing single file or whole directory,
 - take screenshot (Linux) or get picture from clipboard (Windows and MacOS) and use it as source picture,
 - after processing results is copied into clipboard (Windows),
 - display selected tools,
 - tools selection,
 - preview orignal and result,
 - predefined rotation: 90, 180 and 270 degree or custom,
 - crop selection via click on preview or coordinates,
 - crop coordinates:
   - two corners (upper left and lower right),
   - upper left corner and width plus height,
   - gravity, width plus height plus offset,
 - text: color, font and size selection, background, rotation,
 - text position:
   - outside: bottom, left/center/right
   - inside: by gravity or by position and rotate
 - customized sepia - only with Wand and ImageMagick,
 - equalize by channel,
 - contrast between -5 and +5,
 - customized contrast stretching,
 - vignette:
   - can be sharp or blured, 
   - corners can be filled by selected color,
   - offset in both direction
 - logo position by gravity, size and offset,
 - compose:
   - add picture on right side
   - add picture on bottom
   - autoresize picture
   - fill color if no autoresize
 - fast file navigation: First, Prev, Next, Last or keys: Home, PgUp, PgDn, End,
 - command editor: possible to use ImageMagick commands for convert: eg. *-gaussian-blur 10x10* or *-monochrome*, etc.
- dark and light mode

---

## Processing

Is possible to run one conversion or all selected conversion.
Processing order for all selected conversion:

- crop,
- mirror,
- black-white,
- sepia - only with Wand and ImageMagick,
- contrast,
- color normalize,
- vignette - only with Wand and ImageMagick,
- rotate,
- border,
- resize,
- text - only with Wand and ImageMagick,
- logo - only with Wand and ImageMagick.

Processed is always on clone of picture in memory. Originals are not touched.

## User manual, a bit outdated

- [English](doc/en/fotokilof.md),
- [Polish](doc/pl/fotokilof.md).

## Available translations

Available: Bulgarian, English, German, Indonesian, Polish and Turkish.

---

## Install and run

### Requirements

- Windows, Linux, MacOS X, BSD,
- FullHD screen for comfort work,
- [ImageMagick](https://imagemagick.org/), remember to add path into `%PATH%` environment variable, enable install libraries!
- [Python3.9+](https://www.python.org/), remember to add path into `%PATH%` environment variable.

### Install

#### Linux

Install requirements:
```bash
apt-get install python3-pip python3-tk python3-wand imagemagick
```

Install as PyPi package by PIP:
```bash
python3 -m pip install fotokilof
```

#### Windows
Download and install requirements:
- [Python3.9+](https://www.python.org/) - add path into `%PATH%` environment variable,
- [ImageMagick](https://imagemagick.org/script/download.php#windows) - add path into `%PATH%` environment variable, enable install libraries!

```bash
python -m pip install pywin32 fotokilof
```

#### MacOS
Install requirements:
```bash
brew install imagemagick python@3.12 python-tk@3.12
```

For Apple Silicon (M1, M2, M3) based Macs, the default Homebrew install directory differs from that on Homebrew Intel installs. The following environment variable allows FotoKilof to correctly locate the Homebrew-installed ImageMagick on Apple Silicon Macs:
```bash
export MAGICK_HOME=/opt/homebrew
```

Install as PyPi package by PIP:
```bash
python3 -m pip install fotokilof
```

#### FreeBSD

FotoKilof is available via [ports](https://www.freshports.org/graphics/py-fotokilof/)

### Upgrade

```bash
python3 -m pip install --upgrade fotokilof
```

### Run

```bash
fotokilof
```
or
```bash
python -m fotokilof
```

### Dark or Light mode

Press F2 to toggle from Light to Dark or opposite.

---

## Thanks

 - Friends - some ideas and testing,
 - Max von Forell - German translation,
 - Bozhidar Kirev - Bulgarian translation,
 - Alexander Ignatov - Bulgarian translation,
 - Afif Hendrawan - Indonesian translation,
 - Sebastian Hiebl - python packaging,
 - Matt Sephton - ideas for packing gui,
 - emsspree - update german translation, jpeg,
 - Olm - testing on Windows,
 - Carbene Hu - idea to fix issue
 - Mert Cobanov - Turkish translation
 - Giancarlo Dessì - Italian translation, Slackware package
 - Danny (dchenz) - logging in proper way

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=TeaM-TL/FotoKilof&type=Date)](https://star-history.com/#TeaM-TL/FotoKilof&Date)

---

## Powered by

![Python powered](python-powered.png) 
[Imagemagick](https://github.com/ImageMagick/ImageMagick) 
[Wand](https://github.com/emcconville/wand) 
[ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) 

