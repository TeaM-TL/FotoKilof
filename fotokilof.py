# -*- coding: utf-8 -*-
# $Id: fotokilof.py 19 2019-09-06 11:39:29Z tlu $

import datetime
import platform
import os
import sys
import shutil
import re
import configparser
import glob

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkcolorpicker import askcolor

from PIL import Image

###################
# Stałe
PREVIEW = 500  # rozmiar obrazka podglądu
VERSION = 1.6  # wersja programu

##########################


def no_text_in_windows():
    if(platform.system() == "Windows"):
        l_text_windows.configure(text="Niestety używasz Windows,umieszczanie tekstu może nie działać poprawnie")
        cb_text_font.configure(state='disabled')

    else:
        # cb_text_font.configure(state='readonly')
        print("Uff, nie Windows")


def pre_imagick(file_in_path):
    """
    file_in_path - oryginał do mielenia, pełna ścieżka
    out_file - plik do mielenia, pełna ścieżka
    """
    global work_dir
    # Zakładanie katalogu na obrazki wynikowe - podkatalog folderu z obrazkiem
    out_dir = os.path.join(os.path.dirname(file_in_path), work_dir)
    if(os.path.isdir(out_dir) is False):
        try:
            os.mkdir(out_dir)
            print("Out_dir: " + out_dir)
        except:
            print("Nie można utworzyć katalogu na przemielone rysunki")
            return

    # Kopiowanie oryginału do miejsca mielenia
    out_file = os.path.join(out_dir, os.path.basename(file_in_path))
    # adding exception handling
    try:
        shutil.copyfile(file_in_path, out_file)
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)
    return out_file


def imagick(cmd, out_file):
    """
    cmd - polecenie imagemagick
    out_file - obrazek do mielenia, pełna ścieżka
    """

    out_file = spacja(out_file)
    command = "mogrify " + cmd + " " + out_file
    print(command)
    try:
        os.system(command)
    except:
        print("Error in imagick: " + command)

################
# Preview


def preview_histogram(file):
    global temp_dir

    file_histogram = spacja(os.path.join(temp_dir, os.path.basename(file) + ".png"))
    file = spacja(file)

    command = "convert " + file + " -colorspace Gray -define histogram:unique-colors=false histogram:" + file_histogram
    print(command)
    try:
        os.system(command)
        return file_histogram
    except:
        print("Error in convert_histogram: " + command)


def preview_orig_bind(event):
    global file_in_path, temp_dir
    preview_orig(file_in_path.get(), temp_dir)


def preview_orig(file_in_path, temp_dir):
    # generowanie podglądu oryginału

    preview = convert_preview(file_in_path, temp_dir)
    try:
        pi_preview_orig.configure(file=preview['filename'])
        l_preview_orig.configure(text=preview['width'] + "x" + preview['height'])
    except:
        print("Nie można wczytać podglądu")

    try:
        pi_histogram_orig.configure(file=preview_histogram(file_in_path))
    except:
        print("Error in preview histogram_new")


def preview_new(out_file, temp_dir):
    # generowanie podglądu wynikowego

    preview = convert_preview(out_file, temp_dir)
    try:
        pi_preview_new.configure(file=preview['filename'])
        l_preview_new.configure(text=preview['width'] + "x" + preview['height'])
        os.remove(preview['filename'])
    except:
        print("Nie można wczytać podglądu")

    try:
        pi_histogram_new.configure(file=preview_histogram(out_file))
    except:
        print("Error in preview histogram_new")


def preview_orig_button():
    #    podgląd oryginału
    global file_in_path

    try:
        img = Image.open(file_in_path.get())
        img.show()
    except:
        print("Chyba nie ma obrazka")


def preview_new_button():
    #    podgląd wynikowego obrazka
    global file_in_path, work_dir

    file_show = os.path.join(os.path.dirname(file_in_path.get()),
                             work_dir, os.path.basename(file_in_path.get()))
    try:
        img = Image.open(file_show)
        img.show()
    except:
        print("Chyba nie ma obrazka")


def convert_preview(file, temp_dir):
    """
    generowanie podglądu oryginału
    file - nazwa obrazka, pełna ścieżka
    temp_dir - katalog tymczasowy, pełna ścieżka

    zwraca: nazwę podglądu obrazka i rozmiar
    """

    # im = Image.open(spacja(file))
    im = Image.open(file)
    width = str(im.size[0])
    height = str(im.size[1])

    filename, file_extension = os.path.splitext(file)
    file_preview = os.path.join(temp_dir, os.path.basename(filename) + ".ppm")

    file = spacja(file)
    file_preview = spacja(file_preview)

    command = "convert " + file + " -resize " + str(PREVIEW) + "x" + str(PREVIEW) + " " + file_preview
    print(command)
    try:
        os.system(command)
    except:
        print("Error in convert_preview: " + command)

    try:
        return {'filename': file_preview, 'width': width, 'height': height}
    except:
        return "Error in convert_preview: return"

    
def spacja(sciezka):
    # rozwiązanie problemu spacji w nazwach plików i katalogów

    sciezka = os.path.normpath(sciezka)
    if(platform.system() == "Windows"):
        sciezka = '"' + sciezka + '"'
    else:
        sciezka = re.sub(' ', '\ ', sciezka)
    return sciezka


def apply_all_convert(out_file):
    #    zaaplikowanie wszystkich opcji na raz

    convert_normalize(out_file)
    convert_contrast(out_file)
    convert_bw(out_file)
    convert_rotate(out_file)
    if(int(img_resize.get()) > 0):
        convert_resize(out_file)
    else:
        convert_crop(out_file)
    convert_border(out_file)
    convert_text(out_file)


def apply_all():
    #    zaplikowanie wszystkich opcji na raz
    global file_in_path, temp_dir, out_dir, file_dir_selector, progress_files, progress_filename

    if(file_dir_selector.get() == 0):
        out_file = pre_imagick(file_in_path.get())
        progress_filename.set(out_file)
        apply_all_convert(out_file)
        preview_new(out_file, temp_dir)
        progress_filename.set("")
    else:
        pwd = os.getcwd()
        os.chdir(os.path.dirname(file_in_path.get()))
        i = 0
        for files in glob.glob("*.[j|J][p|P][g|G]"):
            i = i + 1
            print(i)
            progress_files.set(str(i) + " z ")
            out_file = pre_imagick(files)
            progress_filename.set(out_file)
            apply_all_convert(os.path.realpath(out_file))
        progress_files.set("")
        progress_filename.set(" ")
        preview_new(out_file, temp_dir)
        os.chdir(pwd)

        
def contrast_selected(event):
    # wywołanie przez bind
    global img_contrast_selected
    print('You selected:', cb_contrast.get())
    img_contrast_selected.set(cb_contrast.get())


def convert_contrast_button():
    #
    global file_in_path, temp_dir, out_dir
    out_file = pre_imagick(file_in_path.get())
    convert_contrast(out_file)
    preview_new(out_file, temp_dir)


def convert_contrast(out_file):
    #    Normalizacja kolorów
    global img_contrast, img_contrast_selected

    if(img_contrast.get() == 1):
        if(img_contrast_selected.get() == "+2"):
            command = "+contrast +contrast"
        elif(img_contrast_selected.get() == "+1"):
            command = "+contrast"
        elif(img_contrast_selected.get() == "-1"):
            command = "-contrast"
        elif(img_contrast_selected.get() == "-2"):
            command = "-contrast -contrast"
        else:
            return
        imagick(command, out_file)
    elif(img_contrast.get() == 2):
        command = "-contrast-stretch " + e1_contrast.get() + "x" + e2_contrast.get() + "%"
        imagick(command, out_file)


def convert_bw_button():
    #
    global file_in_path, temp_dir, out_dir
    out_file = pre_imagick(file_in_path.get())
    convert_bw(out_file)
    preview_new(out_file, temp_dir)


def convert_bw(out_file):
    #    Normalizacja kolorów
    global img_normalize
    if(img_bw.get() == 1):
        command = "-colorspace Gray"
        # command = "separate"
        imagick(command, out_file)
    elif(img_bw.get() == 2):
        command = "-sepia-tone " + str(int(e_bw_sepia.get())) + "%"
        imagick(command, out_file)


def convert_normalize_button():
    #
    global file_in_path, temp_dir, out_dir
    out_file = pre_imagick(file_in_path.get())
    convert_normalize(out_file)
    preview_new(out_file, temp_dir)


def convert_normalize(out_file):
    #    Normalizacja kolorów
    global img_normalize
    if(img_normalize.get() == 1):
        command = "-normalize"
        imagick(command, out_file)
    elif(img_normalize.get() == 2):
        command = "-auto-level"
        imagick(command, out_file)


def convert_rotate_button():
    #
    global file_in_path, temp_dir, out_dir
    out_file = pre_imagick(file_in_path.get())
    convert_rotate(out_file)
    preview_new(out_file, temp_dir)


def convert_rotate(out_file):
    #    Obrót obrazka o 90,180 albo 270stopni
    global img_rotate
    if(img_rotate.get() > 0):
        # chciałem ImageTk ale nie działa
        # im = Image.open(out_file)
        # im.rotate(img_rotate.get())
        # im.save(out_file)
        command = "-rotate " + str(img_rotate.get())
        imagick(command, out_file)


def convert_resize_button():
    #
    global file_in_path, temp_dir, out_dir
    out_file = pre_imagick(file_in_path.get())
    convert_resize(out_file)
    preview_new(out_file, temp_dir)


def convert_resize(out_file):
    #    Zmiana rozmiaru obrazka
    global img_resize
    border = 2 * int(e_border.get())
    if(img_resize.get() == 0):
        # print("Nie wybrano rodzaju skalowania")
        return
    elif(img_resize.get() == 1):
        image_resize = e1_resize.get() + "x" + e1_resize.get()
    elif(img_resize.get() == 2):
        image_resize = e2_resize.get() + "%"
    elif(img_resize.get() == 3):
        image_resize = str(1920 - border) + "x" + str(1080 - border)
    elif(img_resize.get() == 4):
        image_resize = str(2048 - border) + "x" + str(1556 - border)
    elif(img_resize.get() == 5):
        image_resize = str(4096 - border) + "x" + str(3112 - border)

    command = "-resize " + image_resize
    imagick(command, out_file)


def convert_crop_button():
    #
    global file_in_path, temp_dir, out_dir
    out_file = pre_imagick(file_in_path.get())
    convert_crop(out_file)
    preview_new(out_file, temp_dir)


def convert_crop(out_file):
    #    Wycięcie obrazka z obrazka
    global file_in_path, temp_dir, out_dir, file_dir_selector, img_crop, img_crop_gravity
    if(img_crop.get() > 0):
        if(img_crop.get() == 1):
            X = str(abs(int(e3_crop_1.get()) - int(e1_crop_1.get())))
            Y = str(abs(int(e4_crop_1.get()) - int(e2_crop_1.get())))
            command = " -crop " + X + "x" + Y + "+" + e1_crop_1.get() + "+" + e2_crop_1.get()
        if(img_crop.get() == 2):
            command = " -crop " + e3_crop_2.get() + "x" + e4_crop_2.get() + "+" + e1_crop_2.get() + "+" + e2_crop_2.get()
        if(img_crop.get() == 3):
            command = " -gravity " + gravity(img_crop_gravity.get()) + " -crop " + e3_crop_3.get() + "x" + e4_crop_3.get() + "+" + e1_crop_3.get() + "+" + e2_crop_3.get()

        imagick(command, out_file)


def convert_text_button():
    #
    global file_in_path, temp_dir, out_dir, file_dir_selector
    out_file = pre_imagick(file_in_path.get())
    convert_text(out_file)
    preview_new(out_file, temp_dir)

def convert_text(out_file):
    #     Umieszczenie napisu na obrazku
    global img_text_gravity, img_text_font, img_text_color, img_text_box, img_text_box_color

    if(img_text.get() == 1):
        size = " -pointsize " + e_text_size.get()
        font = " -font '" + img_text_font.get() + "'"
        color = " -fill \"" + img_text_color.get() + "\""
        gravit = " -gravity " + gravity(img_text_gravity.get())
        x = e_text_x.get()
        y = e_text_y.get()
        # text = " -draw \'text " + x + "," + y + " \"" + e_text.get() + "\"\'"
        text = " -draw \"text " + x + "," + y + " '" + e_text.get() + "'\""
        if(img_text_box.get() == 0):
            box = ""
        else:
            box = " -box \"" + img_text_box_color.get() + "\""
        command = box + color + size + gravit + font + text
        imagick(command, out_file)


def fonts():
    # import nazw fontów dla imagemagicka
    global temp_dir

    if(os.path.isdir(temp_dir) is False):
        try:
            # print("Zakladam katalog na pliki tymczasowe: " + temp_dir)
            os.mkdir(temp_dir)
        except:
            # print("Nie można utworzyć katalogu na pliki tymczasowe")
            return

    if(platform.system() == "Windows"):
        fonts_list = ('Arial')
    else:
        file_font = os.path.join(temp_dir, "fonts_list")

        command = "convert -list font > " + spacja(file_font)
        print(command)
        try:
            os.system(command)
        except:
            print("Error: " + command)
            return

        try:
            file = open(file_font, "r")
            fonts_list = []
            for line in file:
                if(re.search("Font", line) is not None):
                    line = re.sub('^[ ]+Font:[ ]*', "", line)
                    line = re.sub('\n', "", line)
                    fonts_list.append(line)
            file.close()
            os.remove(file_font)
        except:
            print("Error przy wczytywaniu listy fontów")
            fonts_list = ('Helvetica')

    cb_text_font['values'] = fonts_list


def font_selected(event):
    # wywołanie przez bind
    global img_text_font
    print('You selected:', cb_text_font.get())
    img_text_font.set(cb_text_font.get())


def crop_read():
    #    Wczytanie rozmiarów z obrazka
    global file_in_path, img_crop_gravity
    img = Image.open(file_in_path.get())
    x = img.size[0]
    y = img.size[1]
    e1_crop_1.delete(0, "end")
    e1_crop_1.insert(0, "0")
    e2_crop_1.delete(0, "end")
    e2_crop_1.insert(0, "0")
    e3_crop_1.delete(0, "end")
    e3_crop_1.insert(0, x)
    e4_crop_1.delete(0, "end")
    e4_crop_1.insert(0, y)
    e1_crop_2.delete(0, "end")
    e1_crop_2.insert(0, "0")
    e2_crop_2.delete(0, "end")
    e2_crop_2.insert(0, "0")
    e3_crop_2.delete(0, "end")
    e3_crop_2.insert(0, x)
    e4_crop_2.delete(0, "end")
    e4_crop_2.insert(0, y)
    e1_crop_3.delete(0, "end")
    e1_crop_3.insert(0, "0")
    e2_crop_3.delete(0, "end")
    e2_crop_3.insert(0, "0")
    e3_crop_3.delete(0, "end")
    e3_crop_3.insert(0, x)
    e4_crop_3.delete(0, "end")
    e4_crop_3.insert(0, y)
    img_crop_gravity.set("C")


def gravity(gravity):
    if(gravity == "N"):
        gravity = "North"
    if(gravity == "NW"):
        gravity = "Northwest"
    if(gravity == "NE"):
        gravity = "Northeast"
    if(gravity == "W"):
        gravity = "West"
    if(gravity == "C"):
        gravity = "Center"
    if(gravity == "E"):
        gravity = "East"
    if(gravity == "SW"):
        gravity = "Southwest"
    if(gravity == "S"):
        gravity = "South"
    if(gravity == "SE"):
        gravity = "Southeast"

    return gravity


def open_file():
    #    otwarcie pliku obrazka do edycji
    global file_in_path, dir_in_path
    file_in_path.set(filedialog.askopenfilename(title="Wybierz plik do mielenia",
                                                initialdir=dir_in_path.get(),
                                                filetypes=(("jpeg files", "*.jpg"),
                                                           ("JPEG files", "*.JPG"),
                                                           ("all files", "*.*"))))
    file_select_L.configure(text=os.path.basename(file_in_path.get()))
    preview_orig(file_in_path.get(), temp_dir)

    dir_in_path.set(os.path.dirname(file_in_path.get()))


def open_file_next():
    global file_in_path, dir_in_path
    pwd = os.getcwd()
    os.chdir(os.path.dirname(file_in_path.get()))
    list = []
    for file in glob.glob("*.[j|J][p|P][g|G]"):
        list.append(file)
    position = list.index(os.path.basename(file_in_path.get()))
    print(position, list)
    if(position <= len(list) - 2):
        file = list[position + 1]
        file_select_L.configure(text=file)
        file_in_path.set(os.path.join(dir_in_path.get(), file))
        preview_orig(file_in_path.get(), temp_dir)
    os.chdir(pwd)


def open_file_prev():
    global file_in_path, dir_in_path

    pwd = os.getcwd()
    os.chdir(os.path.dirname(file_in_path.get()))
    list = []
    for file in glob.glob("*.[j|J][p|P][g|G]"):
        list.append(file)
    position = list.index(os.path.basename(file_in_path.get()))
    print(position, list)
    if(position > 0):
        file = list[position - 1]
        file_select_L.configure(text=file)
        file_in_path.set(os.path.join(dir_in_path.get(), file))
        preview_orig(file_in_path.get(), temp_dir)
    os.chdir(pwd)


def convert_border_button():
    global file_in_path, temp_dir, out_dir
    out_file = pre_imagick(file_in_path.get())
    convert_border(out_file)
    preview_new(out_file, temp_dir)


def convert_border(out_file):
    global img_border_color
    if(int(e_border.get()) > 0):
        command = "-border " + e_border.get() + " -bordercolor \"" + img_border_color.get() + "\""
        imagick(command, out_file)


def color_choose_border():
    #    Wybór koloru tła
    global img_border_color
    color = askcolor(img_border_color.get())
    if(color[1] is None):
        img_border_color.set("#000000")
    else:
        img_border_color.set(color[1])
        l_border.configure(bg=img_border_color.get())


def color_choose_box_active():
    global img_text_box
    if(img_text_box.get() == 0):
        l_text_font_selected.configure(bg="#000000")
    else:
        l_text_font_selected.configure(bg=img_text_box_color.get())


def color_choose_box():
    #    Wybór koloru tła
    global img_text_box, img_text_box_color
    if(img_text_box.get() != 0):
        color = askcolor(img_text_color.get(), root)
        if(color[1] is None):
            img_text_box_color.set("#FFFFFF")
        else:
            img_text_box_color.set(color[1])
            l_text_font_selected.configure(bg=img_text_box_color.get())


def color_choose():
    #    Wybór koloru
    global img_text_color
    color = askcolor(img_text_color.get(), root)
    if(color[1] is None):
        img_text_color.set("#FFFFFF")
    else:
        img_text_color.set(color[1])
    l_text_font_selected.configure(fg=img_text_color.get())


def ini_read(file_ini):
    # lista wyjściowa
    list_return = {}

    # Obsługa pliku konfiguracyjnego INI

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    # read values from a section
    try:
        file_in_path = config.get('Konfiguracja', 'path')
    except:
        file_in_path = ""
    list_return['file_in_path'] = file_in_path

    try:
        file_dir_selector = config.getint('Konfiguracja', 'file_dir')
    except:
        file_dir_selector = "0"
    list_return['file_dir_selector'] = file_dir_selector

    try:
        img_resize = config.getint('Resize', 'resize')
    except:
        img_resize = "1"
    list_return['img_resize'] = img_resize

    try:
        resize_size_pixel = config.getint('Resize', 'size_pixel')
    except:
        resize_size_pixel = "0"
    e1_resize.delete(0, "end")
    e1_resize.insert(0, resize_size_pixel)

    try:
        resize_size_percent = config.getint('Resize', 'size_percent')
    except:
        resize_size_percent = "0"
    e2_resize.delete(0, "end")
    e2_resize.insert(0, resize_size_percent)

    try:
        img_text = config.getint('Text', 'on')
    except:
        img_text = "1"
    list_return['img_text'] = img_text

    try:
        text = config.get('Text', 'text')
    except:
        text = ""
    e_text.delete(0, "end")
    e_text.insert(0, text)

    try:
        img_text_gravity = config.get('Text', 'gravity')
    except:
        img_text_gravity = "SE"
    list_return['img_text_gravity'] = img_text_gravity

    try:
        img_text_font = config.get('Text', 'font')
    except:
        if(platform.system() == "Windows"):
            img_text_font = "Arial"
        else:
            img_text_font = "Helvetica"
    list_return['img_text_font'] = img_text_font

    try:
        text_size = str(config.getint('Text', 'size'))
    except:
        text_size = 12
    e_text_size.delete(0, "end")
    e_text_size.insert(0, text_size)

    try:
        text_x = config.getint('Text', 'x')
    except:
        text_x = "5"
    e_text_x.delete(0, "end")
    e_text_x.insert(0, text_x)

    try:
        text_y = config.getint('Text', 'y')
    except:
        text_y = "5"
    e_text_y.delete(0, "end")
    e_text_y.insert(0, text_y)

    try:
        text_color = config.get('Text', 'color')
    except:
        text_color = "#FFFFFF"
    list_return['img_text_color'] = text_color
    l_text_font_selected.configure(fg=text_color)

    try:
        img_text_box = config.getint('Text', 'box')
    except:
        img_text_box = 0
    list_return['img_text_box'] = img_text_box

    try:
        text_box_color = config.get('Text', 'box_color')
    except:
        text_box_color = "#000000"
    list_return['img_text_box_color'] = text_box_color
    l_text_font_selected.configure(bg=text_box_color)

    try:
        img_rotate = config.getint('Rotate', 'rotate')
    except:
        img_rotate = "0"
    list_return['img_rotate'] = img_rotate

    try:
        img_crop = config.getint('Crop', 'crop')
    except:
        img_crop = "0"
    list_return['img_crop'] = img_crop

    try:
        crop_x1 = config.getint('Crop', 'x1')
    except:
        crop_x1 = "0"
    e1_crop_1.delete(0, "end")
    e1_crop_1.insert(0, crop_x1)

    try:
        crop_y1 = config.getint('Crop', 'y1')
    except:
        crop_y1 = "0"
    e2_crop_1.delete(0, "end")
    e2_crop_1.insert(0, crop_y1)

    try:
        crop_x2 = config.getint('Crop', 'x2')
    except:
        crop_x2 = "0"
    e3_crop_1.delete(0, "end")
    e3_crop_1.insert(0, crop_x2)

    try:
        crop_y2 = config.getint('Crop', 'y2')
    except:
        crop_y2 = "0"
    e4_crop_1.delete(0, "end")
    e4_crop_1.insert(0, crop_y2)

    try:
        crop_x3 = config.getint('Crop', 'x3')
    except:
        crop_x3 = "0"
    e1_crop_2.delete(0, "end")
    e1_crop_2.insert(0, crop_x3)

    try:
        crop_y3 = config.getint('Crop', 'y3')
    except:
        crop_y3 = "0"
    e2_crop_2.delete(0, "end")
    e2_crop_2.insert(0, crop_y3)

    try:
        crop_X1 = config.getint('Crop', 'XX1')
    except:
        crop_X1 = "0"
    e3_crop_2.delete(0, "end")
    e3_crop_2.insert(0, crop_X1)

    try:
        crop_Y1 = config.getint('Crop', 'YY1')
    except:
        crop_Y1 = "0"
    e4_crop_2.delete(0, "end")
    e4_crop_2.insert(0, crop_Y1)

    try:
        crop_dx = config.getint('Crop', 'dx')
    except:
        crop_dx = "0"
    e1_crop_3.delete(0, "end")
    e1_crop_3.insert(0, crop_dx)

    try:
        crop_dy = config.getint('Crop', 'dy')
    except:
        crop_dy = "0"
    e2_crop_3.delete(0, "end")
    e2_crop_3.insert(0, crop_dy)

    try:
        crop_X2 = config.getint('Crop', 'XX2')
    except:
        crop_X2 = "0"
    e3_crop_3.delete(0, "end")
    e3_crop_3.insert(0, crop_X2)

    try:
        crop_Y2 = config.getint('Crop', 'YY2')
    except:
        crop_Y2 = "0"
    e4_crop_3.delete(0, "end")
    e4_crop_3.insert(0, crop_Y2)

    try:
        img_crop_gravity = config.getint('Crop', 'gravity')
    except:
        img_crop_gravity = "C"
    list_return['img_crop_gravity'] = img_crop_gravity

    try:
        img_border_color = config.get('Border', 'color')
    except:
        img_border_color = "#FFFFFF"
    l_border.configure(bg=img_border_color)
    list_return['img_border_color'] = img_border_color

    try:
        border = config.getint('Border', 'size')
    except:
        border = "0"
    e_border.delete(0, "end")
    e_border.insert(0, border)

    try:
        img_normalize = config.getint('Color', 'normalize')
    except:
        img_normalize = 0
    list_return['img_normalize'] = img_normalize

    try:
        img_bw = config.getint('Color', 'bw')
    except:
        img_bw = 0
    list_return['img_bw'] = img_bw

    try:
        img_bw_sepia = config.getint('Color', 'sepia')
    except:
        img_bw_sepia = "95"
    e_bw_sepia.delete(0, "end")
    e_bw_sepia.insert(0, img_bw_sepia)

    try:
        img_contrast = config.getint('Contrast', 'contrast')
    except:
        img_contrast = "0"
    list_return['img_contrast'] = img_contrast

    try:
        contrast_stretch_1 = config.get('Contrast', 'stretch1')
    except:
        contrast_stretch_1 = "0.15"
    e1_contrast.delete(0, "end")
    e1_contrast.insert(0, contrast_stretch_1)

    try:
        contrast_stretch_2 = config.get('Contrast', 'stretch2')
    except:
        contrast_stretch_2 = "0.05"
    e2_contrast.delete(0, "end")
    e2_contrast.insert(0, contrast_stretch_2)

    return list_return


def ini_read_wraper():
    global file_ini
    ini_entries = ini_read(file_ini)
    file_in_path.set(ini_entries['file_in_path'])
    file_dir_selector.set(ini_entries['file_dir_selector'])
    img_resize.set(ini_entries['img_resize'])
    img_text.set(ini_entries['img_text'])
    img_text_gravity.set(ini_entries['img_text_gravity'])
    img_text_font.set(ini_entries['img_text_font'])
    img_text_box.set(ini_entries['img_text_box'])
    img_rotate.set(ini_entries['img_rotate'])
    img_crop.set(ini_entries['img_crop'])
    img_crop_gravity.set(ini_entries['img_crop_gravity'])
    img_text_color.set(ini_entries['img_text_color'])
    img_text_box_color.set(ini_entries['img_text_box_color'])
    img_border_color.set(ini_entries['img_border_color'])
    img_normalize.set(ini_entries['img_normalize'])
    img_bw.set(ini_entries['img_bw'])
    img_contrast.set(ini_entries['img_contrast'])


def ini_save():
    #     Zapis konfiguracji do pliku INI
    global file_ini, file_in_path, img_text, img_resize, img_text_gravity, img_text_font, img_text_color, img_rotate, img_crop, img_crop_gravity, img_text_box, img_text_box_color

    # przygotowanie zawartości
    config = configparser.ConfigParser()
    config.add_section('Konfiguracja')
    config.set('Konfiguracja', 'path', file_in_path.get())
    config.set('Konfiguracja', 'file_dir', str(file_dir_selector.get()))
    config.add_section('Resize')
    config.set('Resize', 'resize', str(img_resize.get()))
    config.set('Resize', 'size_pixel',   e1_resize.get())
    config.set('Resize', 'size_percent', e2_resize.get())
    config.add_section('Text')
    config.set('Text', 'on',      str(img_text.get()))
    config.set('Text', 'text',    e_text.get())
    config.set('Text', 'gravity', img_text_gravity.get())
    config.set('Text', 'font',    img_text_font.get())
    config.set('Text', 'size',    e_text_size.get())
    config.set('Text', 'color',   img_text_color.get())
    config.set('Text', 'box',     str(img_text_box.get()))
    config.set('Text', 'box_color', img_text_box_color.get())
    config.set('Text', 'x',       e_text_x.get())
    config.set('Text', 'y',       e_text_y.get())
    config.add_section('Rotate')
    config.set('Rotate', 'rotate', str(img_rotate.get()))
    config.add_section('Crop')
    config.set('Crop', 'crop', str(img_crop.get()))
    config.set('Crop', 'x1', e1_crop_1.get())
    config.set('Crop', 'y1', e2_crop_1.get())
    config.set('Crop', 'x2', e3_crop_1.get())
    config.set('Crop', 'y2', e4_crop_1.get())
    config.set('Crop', 'x3', e1_crop_2.get())
    config.set('Crop', 'y3', e2_crop_2.get())
    config.set('Crop', 'XX1',  e3_crop_2.get())
    config.set('Crop', 'YY1',  e4_crop_2.get())
    config.set('Crop', 'dx',  e1_crop_3.get())
    config.set('Crop', 'dy',  e2_crop_3.get())
    config.set('Crop', 'XX2',   e3_crop_3.get())
    config.set('Crop', 'YY2',   e4_crop_3.get())
    config.set('Crop', 'gravity', img_crop_gravity.get())
    config.add_section('Border')
    config.set('Border', 'color', img_border_color.get())
    config.set('Border', 'size',  e_border.get())
    config.add_section('Color')
    config.set('Color', 'normalize', str(img_normalize.get()))
    config.set('Color', 'bw', str(img_bw.get()))
    config.set('Color', 'bw_sepia', e_bw_sepia.get())
    config.add_section('Contrast')
    config.set('Contrast', 'contrast', str(img_contrast.get()))
    config.set('Contrast', 'contrast_stretch_1', e1_contrast.get())
    config.set('Contrast', 'contrast_stretch_2', e2_contrast.get())

    # save to a file
    try:
        with open(file_ini, 'w', encoding='utf-8', buffering=1) as configfile:
            config.write(configfile)
    except:
        print("Error! nie udał się zapis do pliku konfiguracyjnego: " + file_ini)


def help_info(event):
    global pwd
    try:
        license_file = os.path.join(pwd, "License")
        file = open(license_file, "r", encoding="utf8")

        message = ""
        for i in file:
            message = message + i
            file.close
    except:
        print("Error przy wczytywaniu pliku licencji")
        message = "Copyright 2019 Tomasz Łuczak"

    messagebox.showinfo(title="Licencja", message=message)


def help_changelog():
    global pwd
    try:
        license_file = os.path.join(pwd, "Changelog")
        file = open(license_file, "r", encoding="utf8")

        message = ""
        for i in file:
            message = message + i
            file.close
    except:
        print("Error przy wczytywaniu dziennika zmian")
        message = "Zmian było duużo..., i jeszcze będą kolejne..."

    messagebox.showinfo(title="Licencja", message=message)


def close_window():
    root.quit()
    root.destroy()
    sys.exit()


def win_deleted():
    print("closed")
    close_window()


def mouse_crop_calculation(x_preview, y_preview):
    # przeliczenie pikseli podglądu  na piksele oryginału
    global file_in_path
    img = Image.open(file_in_path.get())
    x_orig = img.size[0]
    y_orig = img.size[1]
    img.close

    # x_max, y_max - wymiary podglądu, znamy max czyli PREVIEW
    if(x_orig > y_orig):
        # piksele podglądu, trzeba przeliczyć y_max podglądu
        x_max = PREVIEW
        y_max = x_max*y_orig/x_orig
    elif(y_orig > x_orig):
        # przeliczenie x
        y_max = PREVIEW
        x_max = y_max*x_orig/y_orig
    elif(y_orig == x_orig):
        x_max = PREVIEW
        y_max = PREVIEW

    x = int(x_preview*x_orig/x_max)
    y = int(y_preview*y_orig/y_max)
    print("X,Y", x, y)
    return x, y


def mouse_crop_NW(event):
    # lewy górny narożnik
    x_preview = event.x
    y_preview = event.y
    print("SE preview:", x_preview, y_preview)
    xy = mouse_crop_calculation(x_preview, y_preview)
    e1_crop_1.delete(0, "end")
    e1_crop_1.insert(0, xy[0])
    e2_crop_1.delete(0, "end")
    e2_crop_1.insert(0, xy[1])


def mouse_crop_SE(event):
    # prawy dolny narożnik
    x_preview = event.x
    y_preview = event.y
    print("NW preview:", x_preview, y_preview)
    xy = mouse_crop_calculation(x_preview, y_preview)
    e3_crop_1.delete(0, "end")
    e3_crop_1.insert(0, xy[0])
    e4_crop_1.delete(0, "end")
    e4_crop_1.insert(0, xy[1])


def convert_crop_preview(event):
    # rysuje wycinek na rysunku podglądu
    global file_in_path, temp_dir, img_crop, img_text_box_color

    if(img_crop.get() == 1):
        x0 = int(e1_crop_1.get())
        y0 = int(e2_crop_1.get())
        x1 = int(e3_crop_1.get())
        y1 = int(e4_crop_1.get())
        do_nothing = 0
    elif(img_crop.get() == 2):
        x0 = int(e1_crop_2.get())
        y0 = int(e2_crop_2.get())
        x1 = x0 + int(e3_crop_2.get())
        y1 = y0 + int(e4_crop_2.get())
        do_nothing = 0
    else:
        do_nothing = 1

    if(do_nothing == 1):
        preview_orig(file_in_path.get(), temp_dir)
    else:
        preview = convert_preview(file_in_path.get(), temp_dir)
        fileppm = preview['filename']
        x_orig = int(preview['width'])
        y_orig = int(preview['height'])
        # x_max, y_max - wymiary podglądu, znamy max czyli PREVIEW, zwykle 250
        if(x_orig > y_orig):
            # piksele podglądu, trzeba przeliczyć y_max podglądu
            x_max = PREVIEW
            y_max = x_max*y_orig/x_orig
        elif(y_orig > x_orig):
            # przeliczenie x
            y_max = PREVIEW
            x_max = y_max*x_orig/y_orig
        elif(y_orig == x_orig):
            x_max = PREVIEW
            y_max = PREVIEW

        # print("x0, y0, x1, y1", x0, y0, x1, y1)
        ratio_X = x_max / int(x_orig)
        ratio_Y = y_max / int(y_orig)
        x0 = int(x0 * ratio_X)
        y0 = int(y0 * ratio_Y)
        x1 = int(x1 * ratio_X)
        y1 = int(y1 * ratio_Y)

        # print("x0, y0, x1, y1", x0, y0, x1, y1)
        color = " -fill \"" + img_text_box_color.get() + "\""
        line = " -draw 'line "

        x0y0x1y1 = str(x0) + ", 0 " + str(x0) + ", " + str(PREVIEW)
        command = color + line + x0y0x1y1 + "'"
        imagick(command, fileppm)
        x0y0x1y1 = str(x1) + ", 0 " + str(x1) + ", " + str(PREVIEW)
        command = color + line + x0y0x1y1 + "'"
        imagick(command, fileppm)
        x0y0x1y1 = "0, " + str(y0) + " " + str(PREVIEW) + "," + str(y0)
        command = color + line + x0y0x1y1 + "'"
        imagick(command, fileppm)
        x0y0x1y1 = "0, " + str(y1) + " " + str(PREVIEW) + "," + str(y1)
        command = color + line + x0y0x1y1 + "'"
        imagick(command, fileppm)

        try:
            pi_preview_orig.configure(file=fileppm)
        except:
            print("Nie można wczytać podglądu")

###############################################################################
###############################################################################
# okno główne


root = Tk()


root.title("Tomasz Łuczak : FotoKilof : " + str(VERSION) + " : " + str(datetime.date.today()))

style = ttk.Style()
# style = ttk.Style(root)
style.theme_use('clam')

style.configure("Blue.TButton", foreground="blue")
style.configure("Blue.TLabelframe.Label", foreground="blue")

##########################
# Zmienne globalne

work_dir = "FotoKilof"
file_ini = ".fotokilof.ini"
file_dir_selector = IntVar()
file_in_path = StringVar()  # plik obrazka do przemielenia
dir_in_path = StringVar()
img_resize = IntVar()
img_text = IntVar()
img_text_gravity = StringVar()
img_rotate = IntVar()
img_text_font = StringVar()
img_text_font_list = StringVar()
img_text_color = StringVar()
img_text_box = IntVar()
img_text_box_color = StringVar()
img_crop = IntVar()
img_crop_gravity = StringVar()
progress_files = StringVar()
progress_filename = StringVar()
img_border_color = StringVar()
img_normalize = IntVar()
img_bw = IntVar()
img_contrast = IntVar()
img_contrast_selected = StringVar()
pwd = os.getcwd()
temp_dir = os.path.join(pwd, "tmp")

######################################################################
# Karty
######################################################################
nb = ttk.Notebook(root)
nb.pack()
# nb.grid(column=0, row=0, sticky=(N, W, E, S))

# Pierwsza karta
nb1 = ttk.Frame(nb)
nb.add(nb1, text="Łomotanie obrazka")

# Druga karta
nb2 = ttk.Frame(nb)
nb.add(nb2, text="Konfiguracja kilofa")

nb.select(nb1)
nb.enable_traversal()

#####################################################################
# Pierwsza kolumna
#####################################################################
frame_first_col = ttk.Frame(nb1)
frame_first_col.grid(row=1, column=1, rowspan=2, sticky=(N, W, E, S))

###########################
# Wybór obrazka
###########################
frame_input = ttk.Labelframe(frame_first_col, text="Obrazek", style="Blue.TLabelframe")
frame_input.grid(row=1, column=1, columnspan=2, sticky=(N, W, E, S), padx=5, pady=5)
# tworzenie widgetów
file_selector_rb = ttk.Radiobutton(frame_input, text="Plik",
                                   variable=file_dir_selector, value="0")
b_file_select = ttk.Button(frame_input, text="Wybierz plik", command=open_file,
                           style="Blue.TButton")
file_select_L = ttk.Label(frame_input, width=20)
dir_selector_rb = ttk.Radiobutton(frame_input, text="Folder",
                                  variable=file_dir_selector, value="1")
dir_select_L1 = ttk.Label(frame_input, text="Wybrany folder")
dir_select_L = ttk.Label(frame_input, textvariable=dir_in_path, width=40)
b_file_select_next = ttk.Button(frame_input, text="Następny", command=open_file_next)
b_file_select_prev = ttk.Button(frame_input, text="Poprzedni", command=open_file_prev)
# umieszczenie widgetów
file_selector_rb.grid(column=1, row=1, padx=5, pady=5, sticky=W)
b_file_select.grid(column=2, row=1, padx=5, pady=5, sticky=W)
b_file_select_prev.grid(column=3, row=1, padx=5, pady=5, sticky=W)
b_file_select_next.grid(column=4, row=1, padx=5, pady=5, sticky=W)
file_select_L.grid(column=5, row=1, padx=5, pady=5, sticky=W)
#
dir_selector_rb.grid(column=1, row=2, padx=5, pady=5, sticky=W)
dir_select_L1.grid(column=2, row=2, padx=5, pady=5)
dir_select_L.grid(column=3, row=2, columnspan=3, padx=5, pady=5)

###########################
# Resize
###########################
frame_resize = ttk.Labelframe(frame_first_col, text="Skalowanie", style="Blue.TLabelframe")
frame_resize.grid(column=1, row=2, columnspan=2, sticky=(N, W, E, S), padx=5, pady=5)
###
rb_0_resize = ttk.Radiobutton(frame_resize, text="Nic",
                              variable=img_resize, value="0")
rb_1_resize = ttk.Radiobutton(frame_resize, text="Piksele",
                              variable=img_resize, value="1")
e1_resize = ttk.Entry(frame_resize, width=7)
rb_2_resize = ttk.Radiobutton(frame_resize, text="Procenty",
                              variable=img_resize, value="2")
e2_resize = ttk.Entry(frame_resize, width=7)
rb_3_resize = ttk.Radiobutton(frame_resize, text="HD (1920x1080)",
                              variable=img_resize, value="3")
rb_4_resize = ttk.Radiobutton(frame_resize, text="2K (2048×1556)",
                              variable=img_resize, value="4")
rb_5_resize = ttk.Radiobutton(frame_resize, text="4K (4096×3112)",
                              variable=img_resize, value="5")
b_resize = ttk.Button(frame_resize, text="Przeskaluj", style="Blue.TButton",
                      command=convert_resize_button)

rb_0_resize.grid(row=1, column=1, sticky=W, padx=5, pady=5)
rb_1_resize.grid(row=1, column=2, sticky=W, padx=5, pady=5)
e1_resize.grid(row=1, column=3, sticky=W, padx=5, pady=5)
rb_2_resize.grid(row=1, column=4, sticky=W, padx=5, pady=5)
e2_resize.grid(row=1, column=5, sticky=W, padx=5, pady=5)
rb_3_resize.grid(row=2, column=1, columnspan=2, sticky=W, padx=5, pady=5)
rb_4_resize.grid(row=2, column=3, columnspan=2, sticky=W, padx=0, pady=5)
rb_5_resize.grid(row=2, column=5, columnspan=2, sticky=W, padx=0, pady=5)
b_resize.grid(row=1, column=6, sticky=(E), padx=5, pady=5)

############################
# crop
############################
frame_crop = ttk.Labelframe(frame_first_col, text="Wycinek", style="Blue.TLabelframe")
frame_crop.grid(row=3, column=1, columnspan=2, sticky=(N, W, E, S), padx=5, pady=5)
###
rb0_crop = ttk.Radiobutton(frame_crop, text="Nic", variable=img_crop, value="0")
rb1_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="1",
                           text="Współrzędne (x1, y1) i (x2, y2)")
f_clickL_crop = ttk.Labelframe(frame_crop, text="Lewy górny róg")
l_clickL_crop = ttk.Label(f_clickL_crop, text="Kliknij lewym")
e1_crop_1 = ttk.Entry(f_clickL_crop, width=4)
e2_crop_1 = ttk.Entry(f_clickL_crop, width=4)
f_clickR_crop = ttk.Labelframe(frame_crop, text="Prawy dolny róg")
l_clickR_crop = ttk.Label(f_clickR_crop, text="Kliknij prawym")
e3_crop_1 = ttk.Entry(f_clickR_crop, width=4)
e4_crop_1 = ttk.Entry(f_clickR_crop, width=4)

rb2_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="2",
                           text="Współrzędne (x1,y1) i rozmiar (X, Y)")
e1_crop_2 = ttk.Entry(frame_crop, width=4)
e2_crop_2 = ttk.Entry(frame_crop, width=4)
e3_crop_2 = ttk.Entry(frame_crop, width=4)
e4_crop_2 = ttk.Entry(frame_crop, width=4)

rb3_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="3",
                           text="Przesunięcie (dx,dy), rozmiar (X, Y)\ni grawitacja")
e1_crop_3 = ttk.Entry(frame_crop, width=4)
e2_crop_3 = ttk.Entry(frame_crop, width=4)
e3_crop_3 = ttk.Entry(frame_crop, width=4)
e4_crop_3 = ttk.Entry(frame_crop, width=4)

frame_crop_gravity = ttk.Frame(frame_crop)
rbNW_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="NW",
                              variable=img_crop_gravity, value="NW")
rbN_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="N",
                             variable=img_crop_gravity, value="N")
rbNE_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="NE",
                              variable=img_crop_gravity, value="NE")
rbW_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="W",
                             variable=img_crop_gravity, value="W")
rbC_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="Środek",
                             variable=img_crop_gravity, value="C")
rbE_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="E",
                             variable=img_crop_gravity, value="E")
rbSW_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="SW",
                              variable=img_crop_gravity, value="SW")
rbS_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="S",
                             variable=img_crop_gravity, value="S")
rbSE_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="SE",
                              variable=img_crop_gravity, value="SE")

b_crop_read = ttk.Button(frame_crop, text="Wczytaj wpółrzędne z obrazka",
                         command=crop_read)
b_crop = ttk.Button(frame_crop, text="Wytnij", style="Blue.TButton",
                    command=convert_crop_button)

rb0_crop.grid(row=1, column=1, sticky=W, padx=5, pady=5)
f_clickL_crop.grid(row=1, column=2, rowspan=2, columnspan=2, padx=5)
f_clickR_crop.grid(row=1, column=4, rowspan=2, columnspan=2)
l_clickL_crop.grid(row=1, column=1, columnspan=2, sticky=(W, E))
l_clickR_crop.grid(row=1, column=1, columnspan=2, sticky=(W, E))
rb1_crop.grid(row=2, column=1, sticky=W, padx=5, pady=5)
e1_crop_1.grid(row=2, column=1, sticky=W, padx=5, pady=5)
e2_crop_1.grid(row=2, column=2, sticky=W, padx=5, pady=5)
e3_crop_1.grid(row=2, column=1, sticky=W, padx=5, pady=5)
e4_crop_1.grid(row=2, column=2, sticky=W, padx=5, pady=5)
rb2_crop.grid(row=3, column=1, sticky=W, padx=5, pady=5)
e1_crop_2.grid(row=3, column=2, sticky=W, padx=10, pady=5)
e2_crop_2.grid(row=3, column=3, sticky=W, padx=5, pady=5)
e3_crop_2.grid(row=3, column=4, sticky=W, padx=5, pady=5)
e4_crop_2.grid(row=3, column=5, sticky=W, padx=5, pady=5)
rb3_crop.grid(row=4, column=1, sticky=W, padx=5, pady=5)
e1_crop_3.grid(row=4, column=2, sticky=W, padx=10, pady=5)
e2_crop_3.grid(row=4, column=3, sticky=W, padx=5, pady=5)
e3_crop_3.grid(row=4, column=4, sticky=W, padx=5, pady=5)
e4_crop_3.grid(row=4, column=5, sticky=W, padx=5, pady=5)
frame_crop_gravity.grid(row=4, column=6, rowspan=2, columnspan=3)
rbNW_crop_3.grid(row=1, column=1, sticky=W, pady=5)
rbN_crop_3.grid(row=1,  column=2,  pady=5)
rbNE_crop_3.grid(row=1, column=3, sticky=W, pady=5)
rbW_crop_3.grid(row=2,  column=1, sticky=W, pady=5)
rbC_crop_3.grid(row=2,  column=2, sticky=W, pady=5)
rbE_crop_3.grid(row=2,  column=3, sticky=W, pady=5)
rbSW_crop_3.grid(row=3, column=1, sticky=W, pady=5)
rbS_crop_3.grid(row=3,  column=2, pady=5)
rbSE_crop_3.grid(row=3, column=3, sticky=W, pady=5)
b_crop_read.grid(row=5, column=2, columnspan=4, sticky=W, padx=5, pady=5)
b_crop.grid(row=5, column=1, sticky=W, padx=5, pady=5)

###########################
# Tekst
###########################
frame_text = ttk.Labelframe(frame_first_col, text="Dodaj tekst", style="Blue.TLabelframe")
frame_text.grid(row=4, column=1, columnspan=2, sticky=(N, W, E, S), padx=5, pady=5)
###
frame_text_text = ttk.Frame(frame_text)
cb_text = ttk.Checkbutton(frame_text_text, text="Tekst", variable=img_text,
                          onvalue="1", offvalue="0")
e_text = ttk.Entry(frame_text_text, width=50)
frame_text_text.grid(row=1, column=1, columnspan=5, sticky=(W, E))
cb_text.grid(row=1, column=1, sticky=W, padx=5)
e_text.grid(row=1, column=2, sticky=W, padx=5)
###
frame_text_xy = ttk.Frame(frame_text)
l_text_xy = ttk.Label(frame_text_xy, text="Przesunięcie (dx,dy)\nwzględem punktu wstawienia")
e_text_x = ttk.Entry(frame_text_xy, width=3)
e_text_y = ttk.Entry(frame_text_xy, width=3)

frame_text_xy.grid(row=2, column=1)
l_text_xy.grid(row=1, column=1, sticky=W, padx=5)
e_text_x.grid(row=1, column=2, sticky=W, padx=5)
e_text_y.grid(row=1, column=3, sticky=W, padx=5)
###
frame_text_gravity = ttk.Frame(frame_text)
rbNW = ttk.Radiobutton(frame_text_gravity, text="NW",
                       variable=img_text_gravity, value="NW")
rbN = ttk.Radiobutton(frame_text_gravity, text="N",
                      variable=img_text_gravity, value="N")
rbNE = ttk.Radiobutton(frame_text_gravity, text="NE",
                       variable=img_text_gravity, value="NE")
rbW = ttk.Radiobutton(frame_text_gravity, text="W",
                      variable=img_text_gravity, value="W")
rbC = ttk.Radiobutton(frame_text_gravity, text="Środek",
                      variable=img_text_gravity, value="C")
rbE = ttk.Radiobutton(frame_text_gravity, text="E",
                      variable=img_text_gravity, value="E")
rbSW = ttk.Radiobutton(frame_text_gravity, text="SW",
                       variable=img_text_gravity, value="SW")
rbS = ttk.Radiobutton(frame_text_gravity, text="S",
                      variable=img_text_gravity, value="S")
rbSE = ttk.Radiobutton(frame_text_gravity, text="SE",
                       variable=img_text_gravity, value="SE")
frame_text_gravity.grid(row=2, column=2, columnspan=3)
rbNW.grid(row=1, column=1, sticky=W, pady=5)
rbN.grid(row=1,  column=2, pady=5)
rbNE.grid(row=1, column=3, sticky=W, pady=5)
rbW.grid(row=2,  column=1, sticky=W, pady=5)
rbC.grid(row=2,  column=2, pady=5)
rbE.grid(row=2,  column=3, sticky=W, pady=5)
rbSW.grid(row=3, column=1, sticky=W, pady=5)
rbS.grid(row=3,  column=2, pady=5)
rbSE.grid(row=3, column=3, sticky=W, pady=5)
###
frame_text_font = ttk.Frame(frame_text)
cb_text_font = ttk.Combobox(frame_text_font, textvariable=img_text_font)
e_text_size = ttk.Entry(frame_text_font, width=3)
b_text_color = ttk.Button(frame_text, text="Kolor fontu", command=color_choose)
cb_text_box = ttk.Checkbutton(frame_text_font, text="Ramka tła",
                              variable=img_text_box, onvalue="1", offvalue="0",
                              command=color_choose_box_active)
b_text_box_color = ttk.Button(frame_text, text="Kolor ramki",
                              command=color_choose_box)
l_text_windows = ttk.Label(frame_text, width=40)
b_text = ttk.Button(frame_text, text="Umieść tekst", style="Blue.TButton",
                    command=convert_text_button)
l_text_font_selected = Label(frame_text, width=20, textvariable=img_text_font)

l_text_font_selected.grid(row=3, column=1, sticky=(W, E))
b_text_color.grid(row=3, column=3, sticky=(W, E), padx=5, pady=5)
b_text_box_color.grid(row=3, column=4, sticky=(W, E), padx=5, pady=5)
frame_text_font.grid(row=4, column=1, sticky=(W, E))
cb_text_font.grid(row=1, column=1, sticky=(W, E), padx=5)
e_text_size.grid(row=1, column=2, sticky=W, padx=5)
cb_text_box.grid(row=1, column=3, sticky=W, padx=5)
b_text.grid(row=4, column=4, sticky=(W, E), padx=5, pady=5)
l_text_windows.grid(row=5, column=1, columnspan=4, sticky=(W, E))

###########################
# Rotate
###########################
frame_rotate = ttk.Labelframe(frame_first_col, text="Obrót",
                              style="Blue.TLabelframe")
frame_rotate.grid(row=5, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
rb_rotate_0 = ttk.Radiobutton(frame_rotate, text="0",
                              variable=img_rotate, value="0")
rb_rotate_90 = ttk.Radiobutton(frame_rotate, text="90",
                               variable=img_rotate, value="90")
rb_rotate_180 = ttk.Radiobutton(frame_rotate, text="180",
                                variable=img_rotate, value="180")
rb_rotate_270 = ttk.Radiobutton(frame_rotate, text="270",
                                variable=img_rotate, value="270")
b_rotate = ttk.Button(frame_rotate, text="Obróć", style="Blue.TButton",
                      command=convert_rotate_button)

rb_rotate_0.grid(row=1,   column=1, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_90.grid(row=1,  column=2, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_180.grid(row=1, column=3, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_270.grid(row=1, column=4, sticky=(N, W, E, S), padx=5, pady=5)
b_rotate.grid(row=1, column=5, padx=5, pady=5)

############################
# Czarno-białe
############################
frame_bw = ttk.LabelFrame(frame_first_col, text="Czarno-białe",
                          style="Blue.TLabelframe")
frame_bw.grid(row=5, column=2, rowspan=2, sticky=(N, W, E, S), padx=5, pady=5)
###
rb0_bw = ttk.Radiobutton(frame_bw, text="Nic", variable=img_bw, value="0")
rb1_bw = ttk.Radiobutton(frame_bw, text="Czarno-białe", variable=img_bw, value="1")
rb2_bw = ttk.Radiobutton(frame_bw, text="Sepia", variable=img_bw, value="2")
e_bw_sepia = ttk.Entry(frame_bw, width=3)
l_bw_sepia = ttk.Label(frame_bw, text="%")
b_bw = ttk.Button(frame_bw, text="Wykonaj", style="Blue.TButton",
                  command=convert_bw_button)

rb0_bw.grid(row=1, column=1, padx=5, pady=5, sticky=W)
rb1_bw.grid(row=2, column=1, padx=5, pady=5, sticky=W)
rb2_bw.grid(row=3, column=1, padx=5, pady=5, sticky=W)
e_bw_sepia.grid(row=3, column=2, padx=5, pady=5, sticky=E)
l_bw_sepia.grid(row=3, column=3, padx=5, pady=5, sticky=W)
b_bw.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky=E)

###########################
# Border
###########################
frame_border = ttk.Labelframe(frame_first_col, text="Ramka",
                              style="Blue.TLabelframe")
frame_border.grid(row=6, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
l_border = Label(frame_border, text="Piksele")
e_border = ttk.Entry(frame_border, width=3)
b1_border = ttk.Button(frame_border, text="Kolor", command=color_choose_border)
b_border = ttk.Button(frame_border, text="Dodaj ramkę", style="Blue.TButton",
                      command=convert_border_button)
l_border.grid(row=1, column=1, padx=5, pady=5)
e_border.grid(row=1, column=2, padx=5, pady=5)
b1_border.grid(row=1, column=3, padx=5, pady=5)
b_border.grid(row=1, column=4, padx=5, pady=5, sticky=E)

########################################################################
# Druga kolumna
########################################################################
frame_second_col = ttk.Frame(nb1)
frame_second_col.grid(row=1, column=2, sticky=(N, W, E, S))

############################
# Ramka podglądu oryginału
############################
frame_preview_orig = ttk.Labelframe(frame_second_col, text="Oryginał", style="Blue.TLabelframe")
frame_preview_orig.grid(row=1, column=1, columnspan=2, sticky=(N, W, E, S), padx=5, pady=5)
###
b_preview_orig = ttk.Button(frame_preview_orig, text="Oryginał",
                            command=preview_orig_button)
l_preview_orig = ttk.Label(frame_preview_orig)
pi_preview_orig = PhotoImage()
l_preview_orig_pi = ttk.Label(frame_preview_orig, image=pi_preview_orig)
b_preview_orig.grid(row=1, column=1, padx=5, pady=5)
l_preview_orig.grid(row=1, column=2, padx=5, pady=5)
l_preview_orig_pi.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

###########################
# Histogram original
###########################
frame_histogram_orig = ttk.LabelFrame(frame_second_col, text="Histogram")
frame_histogram_orig.grid(row=2, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
pi_histogram_orig = PhotoImage()
l_histogram_orig = ttk.Label(frame_histogram_orig, image=pi_histogram_orig)
l_histogram_orig.grid(row=1, column=1, padx=10, pady=5)

########################
# Kontrast
#########################
frame_contrast = ttk.Labelframe(frame_second_col, text="Kontrast", style="Blue.TLabelframe")
frame_contrast.grid(row=2, column=2, sticky=(N, W, E, S), padx=5, pady=5)
###
rb0_contrast = ttk.Radiobutton(frame_contrast, text="Nic",
                               variable=img_contrast, value="0")
b_contrast = ttk.Button(frame_contrast, text="Kontrast", style="Blue.TButton",
                        command=convert_contrast_button)
rb1_contrast = ttk.Radiobutton(frame_contrast, text="Kontrast",
                               variable=img_contrast, value="1")
cb_contrast = ttk.Combobox(frame_contrast, width=2,
                           values=("+2", "+1", "0", "-1", "-2"))
rb2_contrast = ttk.Radiobutton(frame_contrast, text="Rozciąganie",
                               variable=img_contrast, value="2")
e1_contrast = ttk.Entry(frame_contrast, width=4)
e2_contrast = ttk.Entry(frame_contrast, width=4)
l1_contrast = ttk.Label(frame_contrast, text="Czerń")
l2_contrast = ttk.Label(frame_contrast, text="Biel")

rb0_contrast.grid(row=1, column=1, padx=5, pady=5, sticky=W)
rb1_contrast.grid(row=2, column=1, padx=5, pady=5, sticky=W)
cb_contrast.grid(row=2, column=2, padx=5, pady=5, sticky=W)
rb2_contrast.grid(row=3, column=1, padx=5, pady=5, sticky=W)
e1_contrast.grid(row=4, column=1, padx=5, pady=5, sticky=E)
e2_contrast.grid(row=4, column=2, padx=5, pady=5, sticky=W)
l1_contrast.grid(row=5, column=1, padx=5, pady=5, sticky=E)
l2_contrast.grid(row=5, column=2, padx=5, pady=5, sticky=W)
b_contrast.grid(row=6, column=1, padx=5, pady=5, columnspan=3, sticky=E)


############################
# Normalize
############################
frame_normalize = ttk.LabelFrame(frame_second_col, text="Normalizacja kolorów",
                                 style="Blue.TLabelframe")
frame_normalize.grid(row=3, column=1, columnspan=2, sticky=(N, W, E, S), padx=5, pady=5)
###
rb0_normalize = ttk.Radiobutton(frame_normalize, text="Nic",
                                variable=img_normalize, value="0")
rb1_normalize = ttk.Radiobutton(frame_normalize, text="Normalize",
                                variable=img_normalize, value="1")
rb2_normalize = ttk.Radiobutton(frame_normalize, text="AutoLevel",
                                variable=img_normalize, value="2")
b_normalize = ttk.Button(frame_normalize, text="Normalizuj", style="Blue.TButton",
                         command=convert_normalize_button)

rb0_normalize.grid(row=1, column=1, padx=5, pady=5, sticky=W)
rb1_normalize.grid(row=1, column=2, padx=5, pady=5, sticky=W)
rb2_normalize.grid(row=1, column=3, padx=5, pady=5, sticky=W)
b_normalize.grid(row=1, column=4, padx=5, pady=5, sticky=E)

#####################################################
# Trzecia kolumna
#####################################################
frame_third_col = ttk.Frame(nb1)
frame_third_col.grid(row=1, column=3, sticky=(N, W, E, S))

##########################
# Ramka podglądu wyniku
###########################
frame_preview_new = ttk.Labelframe(frame_third_col, text="Wynik",
                                   style="Blue.TLabelframe")
frame_preview_new.grid(row=1, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
b_preview_new = ttk.Button(frame_preview_new, text="Wynik",
                           command=preview_new_button)
l_preview_new = ttk.Label(frame_preview_new)
pi_preview_new = PhotoImage()
l_preview_new_pi = ttk.Label(frame_preview_new, image=pi_preview_new)
# c_preview_new_pi = Canvas(frame_preview_new, width=300, height=300)
b_preview_new.grid(row=1, column=1, padx=5, pady=5)
l_preview_new.grid(row=1, column=2, padx=5, pady=5)
l_preview_new_pi.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
# c_preview_new_pi.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

###########################
# Histogram new
###########################
frame_histogram_new = ttk.LabelFrame(frame_third_col, text="Histogram")
frame_histogram_new.grid(row=2, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
pi_histogram_new = PhotoImage()
l_histogram_new = ttk.Label(frame_histogram_new, image=pi_histogram_new)
l_histogram_new.grid(row=1, column=1, padx=10, pady=5)


###########################
# Rząd przycisków
###########################
frame_last = ttk.Frame(nb1)
frame_last.grid(row=2, column=2, columnspan=3, sticky=(E, S), padx=5, pady=5)
###
b_last_quit = ttk.Button(frame_last, text="Koniec", command=close_window)
b_last_save = ttk.Button(frame_last, text="Zapisz ustawienia", command=ini_save)
b_last_read = ttk.Button(frame_last, text="Wczytaj ustawienia", command=ini_read_wraper)
b_last_apply = ttk.Button(frame_last, text="Zaaplikuj wszystko",
                          style="Blue.TButton", command=apply_all)

b_last_save.grid(row=1,  column=1, padx=25, pady=10)
b_last_read.grid(row=1,  column=2, padx=25, pady=10)
b_last_apply.grid(row=1, column=3, padx=25, pady=10)
b_last_quit.grid(row=1,  column=4, padx=50, pady=10, sticky=E)

##########################
# Postęp
##########################
l_last_progress_files = ttk.Label(frame_last, textvariable=progress_files)
l_last_progress_filename = ttk.Label(frame_last, textvariable=progress_filename)

l_last_progress_files.grid(row=1, column=6, padx=5)
l_last_progress_filename.grid(row=1, column=7, padx=5)

###############################################################################
###############################################################################

# podpinanie poleceń do widgetów, menu, skrótów
cb_text_font.bind("<<ComboboxSelected>>", font_selected)
cb_contrast.bind("<<ComboboxSelected>>", contrast_selected)
l_preview_orig_pi.bind("<Button-1>", mouse_crop_NW)
l_preview_orig_pi.bind("<Button-3>", mouse_crop_SE)
rb0_crop.bind("<Button-1>", preview_orig_bind)
rb1_crop.bind("<ButtonRelease-1>", convert_crop_preview)
rb2_crop.bind("<ButtonRelease-1>", convert_crop_preview)
rb3_crop.bind("<Button-1>", preview_orig_bind)
root.bind("<F1>", help_info)
root.protocol("WM_DELETE_WINDOW", win_deleted)

###############
# Uruchomienie funkcji
#
ini_read_wraper()  # Wczytanie konfiguracji
fonts()    # Wczytanie dostępnych fontów
no_text_in_windows()  # Ostrzeżenie, jesli Windows
dir_in_path.set(os.path.dirname(file_in_path.get()))  # wczytanie ścieżki
if(os.path.isfile(file_in_path.get())):
    preview_orig(file_in_path.get(), temp_dir)  # Wczytanie podglądu oryginału
    if(img_crop.get() > 0):
        convert_crop_preview("none")

l_border.configure(bg=img_border_color.get())

root.mainloop()

# EOF
