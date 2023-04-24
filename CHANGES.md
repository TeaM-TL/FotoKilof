# Changelog

## 2023

4.3.0 ttkbootstrap - solve many small annoying things, less duplicated code,

4.2.6 removed theme selector, better paned window

4.2.5 very small polishing tkinter, F1 fixed, progressbar works

4.2.4 fix gui, better handle open file, fix crop

## 2022

4.2.3 canvas for preview instead label, info label, fixed preview issue, small code polishing

4.2.2 fixed problem of display preview, cleaning after pylint

4.2.1 better handling color selector, better look if two tools are in the same row, added missing tooltip

4.2.0 added vignette converter, order tools as order of full conversion, unified showing selected color

4.1.1 order in modules, fix error screenshot when crop, fix crop widget display, more tooltips, more error handling

4.1.0 better handling text outside, better resize, fixed screenshot under MacOS, much more tooltips, better code of text

4.0.9 fixed: text outside, contrast

4.0.8 added EXIF strip/keep

4.0.7 fixed preview for resized picture

4.0.6 added rotation of text, tooltips

4.0.5 added gravity for logo, fixed resize conversion if FotoKilof parent directory doesn't exists

4.0.4 fix processing whole directory, fix directory name

4.0.3 some code improvement, PIL only for Windows for clipboard handle

4.0.2 pip works again

4.0.1 small code polishing

4.0.0 use Wand-py instead PIL (almost) or execute magick as process, removed GraphicsMagick, works under Windows 11

3.8.6 added Turkish translations

3.8.5 fix issue #118

3.8.4 fix issue #123

## 2021

3.8.3 mirroring picture

3.8.2 bugfix and code clean for text gravity

3.8.1 bugfix crop and text position calculation

3.8.0 text tool: gravity on/off, point out position

3.7.10 small improvements

3.7.9 faster preview

3.7.8 fixed: right mouse button for crop, crash when crop was active

3.7.7 fixed crash on startup when last used image path does not exist anymore (#108)

3.7.6 more intuitive preview original with crop

3.7.5 more intuitive, less confusing, hide not neccessary widgets

3.7.4 fixed: duplicate mass conversion on Windows, display text colors, better code

3.7.3 add text tool - reorganized layout

3.7.2 bugfix preview on Linux

3.7.1 fonts works properly on Windows, fixed missing pillow dependency

3.7.0 new layout, tools selection has own row instead column

3.6.1 better recognize new version ImageMagick under Windows

3.6.0 faster under Windows (result preview by Pillow), result is copied into clipboard (only Windows), removed progressbar

3.5.9 fixed execute all for png files

3.5.8 multiple filetypes for open file dialog

3.5.7 added jpeg file type, update German translation, minor bugfixes

3.5.6 added key binding for `<Home>`,`<End>`,`<PgUp>`,`<PgDown>` for fast change pictures

3.5.5 no preview for orig or new picture

3.5.4 filename converted file moved into window title

## 2020

3.5.3 fixed start for MS Windows (disable check magick import), getting picture from clipboard instead screenshot (Windows)

3.5.2 fixed setup.py for PyPi

3.5.1 disable screenshot under MS Windows, disable screenshot if IM is unavailable

3.5.0 take and use screenshots (window or selection), screenshot are stored in `$TMP` or `%TEMP%`

3.4.0 resized pictures are in subfolders, catching more exception

3.3.2 remove not necessary modules: getpass, pathlib

## 2019

3.3.1 GUI user friendly, preview new (if exists) during navigation, clear preview

3.3 Added: paned frames, reorder GUI

3.2 Added: text inside and outside, logging. Small code review, standarize temporary file

3.1 scalable preview widgets, format conversion, SVG conversion, code standarization, speedup, bug_fix, removed Pillow module,

3.0 Order with Contrast and Normalize, updated documentation, fixed INI reading

2.9.6 Added preview crop, updated documentation

2.9.5 .INI is in $HOME directory; crop and text work together properly

2.9.4 `$TMP` instead own temporary directory

2.9.3 Added: option -equalize for Normalize, clean button for custom field

2.9.2 Added: picture size, bug fixing

2.9.1 Hardening: parsing INI entries against data out of range

2.9 Added: GraphicsMagick support, Indonesian translation, code clean

2.8 Added: custom command to execute, theme selection, bugfix

2.7 Added: progressbar

2.6 Added: insert logo on picture

2.5 GUI: cleanup and order

2.4 Added: German translation

2.3 localization via gettext

2.2 split main file into modules, code cleaning (pylint 7.74)

2.1 code cleaning - pylint (jump from 3.87 to 7.03), histogram on/off

2.0 faster multiple conversion: one run of imagemagick, way for creating plugins

1.9.2 Deleted: ttk:notebook

1.9.1 Added: new buttons: First, Last, order in GUI

1.9 Added: menu for tool selection

1.8 better reliability

1.7 better preview conversion

1.6 Added: new buttons: Next, Previous, project on GitHub!

1.5 order in GUI

1.4 Added: histograms for original and result

1.3 Added: click in preview for crop coordinates, menubar deleted

1.2 b-w, sepia, contrast, widgetname standarization

1.1 Added: resize option (HD, 2K, 4K), autoload preview, new conversion: frame, color normalize. Again workaround space in paths and read/write INI

1.0 Added: conversion whole directory

0.9 better and cleaner code

0.8 mogrify instead convert, first copy picture, later work on picture in destination folder

0.7 workaround space in path and filename
(works under Windows, Linux), correct read/write INI

0.6 Added: multiple conversions

0.5 works under Windows, except text

0.4 Added preview, ImageMagick instead PIL

0.3 all conversions work

0.2 Added: font selection, PIL library

0.1 first GUI

0 - start in 2019 August
