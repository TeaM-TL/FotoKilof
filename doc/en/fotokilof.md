**Tomasz Łuczak**

# FotoKilof

------

[TOC]

## Introduction
GUI for the common used ImageMagick functionality for processing pictures.

### Conversions
 - rotation (90, 180, 270 degree)
 - frame around picture
 - text annotation
 - black-white or sepia conversion
 - contrast or histogram stretching
 - color normalize/auto-level
 - crop (three ways selection)
 - scaling/resize: own size (in pixel or percent) or predefined: HD, 2k, 4k
 - adding logo image o picture

### Functionality:
 - processing copy of picture, originals are safe
 - processing single file or whole directory,
 - display selected tools,
 - tools selection
 - preview
 - crop selection via click on preview or coordinates, in three ways
 - text: color, font and size selection (Linux, Mac OSX only)
 - fast file navigation: First, Prev, Next, Last
 - histograms of original and result pictures
 - own command editor, additionaly commands can be composed from started commands

### Screenshots

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof1.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof2.png)

## How to use it

### Resize

### Crop

### Text

### Rotate

### Border

### Black-white/Sepia

### Colors normalize

### Contrast

### Histogram

### Custom conversion

### One file or whole directory

## Installation

### Windows
- Unzip *fotokilof.zip* into folder, 
- make shortcut to desktop,
- and run
 > In future should be available installer package,  by NSIS.

### Linux, MacOSX, *BSD
* unzip and run

### Requirement
 - ImageMagick - home page: https://imagemagick.org/
 - Windows, Linux, MacOS X, BSD
 - FullHD screen for comfort work

### From sources
only for launch sources

#### Python3 and modules
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

#### Start
`python3 fotokilof.py

## Thanks

 - Friends - for inspiration and advices,
 - Max von Forell - German translation
 - Bozhidar Kirev - Bulgarian translation
 - Afif Hendrawan - Indonesian translation