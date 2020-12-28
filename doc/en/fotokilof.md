**Tomasz Łuczak**

# FotoKilof

------

[TOC]

## Introduction
GUI for the common used ImageMagick functionality for processing pictures.

### Conversions
 - scaling/resize, but keep proportion,
 - crop,
 - text annotation (inside or outside of picture),
 - border around picture,
 - rotation,
 - black-white or sepia,
 - contrast inxrease/decrease or normalize or histogram stretching,
 - color normalize: auto-level or equalize,
 - adding logo image o picture.

## Functionality:
 - processing JPG, PNG, SVG and TIF images,
 - conversion into JPG, PNG and TIF format,
 - processing copy of picture, originals are safe,
 - processing single file or whole directory,
 - make screenshots (Linux, macOS) or get picture from clipboard (Windows)
 - display selected tools,
 - tools selection,
 - preview orignal and result,
 - resize custom (pixels or percent) or predefined: FullHD, 2k, 4k,
 - crop selection via click on preview or coordinates,
 - crop coordinates:
   - two corners (upper left and lower right),
   - upper left corner and width plus height,
   - gravity, width plus height plus offset,
 - text: color, font and size selection,
 - predefined rotation: 90, 180 and 270 degree or custom,
 - customized sepia,
 - equalize by channel,
 - contrast between -3 and +3,
 - customized contrast stretching,
 - histograms of original and result pictures,
 - fast file navigation: First, Prev, Next, Last,
 - own command editor,
 - own command can be composed from executed commands,
 - is possible to use other ImageMagick commands, eg. *-gaussian-blur*,
 - logging conversion and internal messages,
 - GraphickMagick is supported partialy.

### Screenshots

#### Linux
![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof.png)

![Screenshot](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof1.png)

#### Mac OSX
![Screenshot MacOS](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_macos.png)

#### Windows
![Screenshot Windows](https://raw.githubusercontent.com/TeaM-TL/FotoKilof/master/screenshots/fotokilof_windows.png)

## How to use it

 - Select image file,
 - Buttons *Previous* and *Next* will open previos or next picture,
 - Select required conversion,
 - Click *Execute*.

### Make screenshots

- Click button *Screenshot*,
- Click (select) window for screenshot.
- or Click and drag for selection rectangle for screenshot.
- Taken picture appear in preview in FotoKilof.
- Screenshot are automatically saved in directory *$TMP/%Y-%m-%D*, eg. /tmp/2020-12-26.
- Result picture is saved in sudirectory *FotoKilof*.

### Resize
Scaling/resize, but keep proportion.
Resize can use custom or predefined values: FullHD, 2k, 4k. Percent means percent size of original picture.

### Crop

Cut rectangular region of the image.

Crop methods:
 - two corners (upper-left and lower-right),
 - upper-left corner and width plus height,
 - gravity, width plus height plus offset.

Remember that upper-left coordinates of original picture are (0, 0).

Coordinates is possible to type in fields or select via click on preview.

*Preview* button will show crop rectangle on preview.

### Text
Annotate an image with text.
Is possible to choose color, font and size. Additionaly is possible to setup background with own color.

Coordinates are given as gravity plus offset.

### Rotate
Apply Paeth image rotation (using shear operations) to the image.

Predefined dvalues: 90, 180 and 270 degrees. In *Custom comands* is possible to type any degree.

### Border
Surround the image with a border of color. Is possible to choose color and type width of border (in pixels).

### Black-white/Sepia

#### Black-white
Convert image to grayscale

#### Sepia
simulate a sepia-toned photo.

Specify threshold as the percent threshold of the intensity (0 - 99.9%). Advice from ImageMagick documentation: a threshold of 80% is a good starting point for a reasonable tone.

### Colors normalize

#### AutoLevel
Automagically adjust color levels of image

#### Equalize
Perform histogram equalization on the image channel-by-channel.

### Contrast

#### Contrast
Enhance or reduce the image contrast. Range is beetween -3 and +3.

#### Contrast stretch
Increase the contrast in an image by stretching the range of intensity values.

#### Normalize
Increase the contrast in an image by stretching the range of intensity values.

### Histogram

### Custom conversion

### One file or whole directory

## Installation

### As pypi package

```
python3 -m pip install fotokilof
fotokilof
```

### From zip

- Unzip *fotokilof.zip* into folder, 
- make shortcut to desktop,
- and run
 > In future should be available installer package, by NSIS.

### Requirement
 - FullHD screen for comfort work
 - ImageMagick - home page: https://imagemagick.org/ or GraphicsMagick
 - Windows, Linux, MacOS X, BSD

### From sources
Only for launch sources

Python3 and modules:
 - via pip:
    - configparser,
    - tkcolorpicker (not mandatory, require PIL).
    - PIL for Windows
 - via packets:
     - tkinter,
 - should be out of the box:
     - datetime,
     - fnmatch,
     - gettext,
     - glob,
     - os,
     - platform,
     - re,
     - shutil,
     - tempfile.

#### Start
`python3 fotokilof.py

## Thanks

 - Friends - for inspiration, advices and testing,
 - Max von Forell - German translation,
 - Bozhidar Kirev - Bulgarian translation,
 - Alexander Ignatov - Bulgarian translation,
 - Afif Hendrawan - Indonesian translation,
 - Sebastian Hiebl - python packaging.
 - Max von Forell - German translation
 - Bozhidar Kirev - Bulgarian translation
 - Afif Hendrawan - Indonesian translation

## License

MIT License

Copyright (c) 2019-2020 Tomasz Łuczak, TeaM-TL

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
