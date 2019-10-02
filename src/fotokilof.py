# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

"""
program do konwersji rysunków
"""

import configparser
import datetime
import gettext
import glob
import platform
import os
import re
import shutil
import sys

from tkinter import TclError, Tk, StringVar, IntVar, N, S, W, E
from tkinter import Label, PhotoImage, filedialog, messagebox, ttk
from tkcolorpicker import askcolor
from PIL import Image

import convert
import common
import ini_read

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
gettext.install('fotokilof', localedir)
translate = gettext.translation('fotokilof', localedir, fallback=True)
_ = translate.gettext
print(localedir)
###################
# CONSTANTS
VERSION = "2.3"
if platform.system() == "Windows":
    PREVIEW = 400  # preview size in Windows
else:
    PREVIEW = 450  # preview size

##########################


def no_text_in_windows():
    """ info dla Windows, że może być problem z dodaniem tekstu """
    if platform.system() == "Windows":
        l_text_windows.configure(text=_("Unfortunately, you are using Windows, thus not all option will work"))
        cb_text_font.configure(state='disabled')

    else:
        cb_text_font.configure(state='readonly')
        # print("Uff, nie Windows")


def pre_imagick(file_in):
    """
    file_in - oryginał do mielenia, pełna ścieżka
    file_out - plik do mielenia, pełna ścieżka
    """
    # global work_dir
    # Zakładanie katalogu na obrazki wynikowe - podkatalog folderu z obrazkiem
    out_dir = os.path.join(os.path.dirname(file_in), work_dir.get())
    if os.path.isdir(out_dir) is False:
        try:
            os.mkdir(out_dir)
        except:
            print("! Error in pre_imagick: Nie można utworzyć katalogu na przemielone rysunki")
            return None

    # Kopiowanie oryginału do miejsca mielenia
    file_out = os.path.join(out_dir, os.path.basename(file_in))
    try:
        shutil.copyfile(file_in, file_out)
    except IOError as error:
        print("! Error in pre_imagick: Unable to copy file. %s" % error)
        exit(1)
    except:
        print("! Error in pre_imagick: Unexpected error:", sys.exc_info())
        exit(1)
    return file_out


def imagick(cmd, file_out):
    """
    uruchomienie imagemagick
    cmd - polecenie dla imagemagick
    file_out - obrazek do mielenia, pełna ścieżka
    """
    if cmd != "":
        file_out = common.spacja(file_out)
        command = "mogrify " + cmd + " " + file_out
        print(command)
        try:
            os.system(command)
        except:
            print("! Error in imagick: " + command)
    else:
        print("puste polecenie dla imagick")

################
# Preview


def preview_histogram(file):
    """ generowanie histogramu """
    # global TEMP_DIR

    file_histogram = common.spacja(os.path.join(TEMP_DIR, "histogram.png"))
    file = common.spacja(file)

    command = "convert " + file + " -colorspace Gray -define histogram:unique-colors=false histogram:" + file_histogram
    print(command)
    try:
        os.system(command)
        return file_histogram
    except:
        print("! Error in convert_histogram: " + command)


def preview_orig_bind(event):
    """ podgląd oryginału wywoałanie via bind """
    # global file_in_path, TEMP_DIR
    preview_orig()


def preview_new(file_out, dir_temp):
    """ generowanie podglądu wynikowego """
    # global img_histograms
    preview = convert_preview(file_out, dir_temp, " ")
    try:
        pi_preview_new.configure(file=preview['filename'])
        l_preview_new.configure(text=preview['width'] + "x" + preview['height'])
        # os.remove(preview['filename'])
    except:
        print("! Error in preview_new: Nie można wczytać podglądu")

    if img_histograms.get() == 1:
        try:
            pi_histogram_new.configure(file=preview_histogram(file_out))
        except:
            print("! Error in preview histogram_new")
    else:
        print("Bez histogramu")


def preview_orig_button():
    """ podgląd oryginału """
    # global file_in_path

    try:
        img = Image.open(file_in_path.get())
        img.show()
    except:
        print("Chyba nie ma obrazka")


def preview_new_button():
    """ podgląd wynikowego obrazka """
    # global file_in_path, work_dir

    file_show = os.path.join(os.path.dirname(file_in_path.get()),
                             work_dir.get(), os.path.basename(file_in_path.get()))
    try:
        img = Image.open(file_show)
        img.show()
    except:
        print("Chyba nie ma obrazka")


def convert_preview(file, dir_temp, command):
    """
    generowanie podglądu oryginału
    file - nazwa obrazka, pełna ścieżka
    dir_temp - katalog tymczasowy, pełna ścieżka
    dodatkowe polecenie dla imagemagick, np. narysuj ramkę crop albo spacja!
    zwraca: nazwę podglądu obrazka i rozmiar
    """

    img = Image.open(file)
    width = str(img.size[0])
    height = str(img.size[1])

    # filename, file_extension = os.path.splitext(file)
    file_preview = os.path.join(dir_temp, "preview.ppm")
    file = common.spacja(file)
    file_preview = common.spacja(file_preview)

    command = "convert " + file + " -resize " + str(PREVIEW) + "x" + str(PREVIEW) + command + file_preview
    print(command)
    try:
        os.system(command)
    except:
        print("! Error in convert_preview: " + command)

    try:
        return {'filename': file_preview, 'width': width, 'height': height}
    except:
        return "! Error in convert_preview: return"


def apply_all_convert(out_file):
    """ zaaplikowanie wszystkich opcji konwersji na raz """
    # global img_rotate, img_resize, img_contrast, img_contrast_selected
    # global img_normalize, img_bw, img_crop, img_crop_gravity
    # global img_text_gravity, img_text_font, img_text_color
    # global img_text_box, img_text_box_color

    cmd = ""
    cmd = cmd + " " + convert.convert_normalize(img_normalize.get())
    cmd = cmd + " " + convert.convert_contrast(img_contrast.get(), img_contrast_selected.get(), e1_contrast.get(), e2_contrast.get())
    cmd = cmd + " " + convert.convert_bw(img_bw.get(), e_bw_sepia.get())
    if int(img_resize.get()) > 0:
        cmd = cmd + " " + convert.convert_resize(img_resize.get(), e1_resize.get(), e2_resize.get(), e_border.get())
    else:
        cmd = cmd + " " + convert.convert_crop(img_crop.get(), img_crop_gravity.get(), convert_crop_entries())
    cmd = cmd + " " + convert.convert_rotate(img_rotate.get())
    cmd = cmd + " " + convert.convert_border(e_border.get(), img_border_color.get())
    imagick(cmd, out_file)

    # ze wzgledu na grawitację tekstu, która gryzie sie z cropem
    # musi być drugi przebieg

    cmd = convert.convert_text(convert_text_entries())
    imagick(cmd, out_file)


def apply_all():
    """
    zaplikowanie wszystkich opcji na raz
    mieli albo plik albo cały katalog
    """
    # global file_in_path, TEMP_DIR, file_dir_selector
    # global progress_files, progress_filename

    if file_dir_selector.get() == 0:
        out_file = pre_imagick(file_in_path.get())
        progress_filename.set(out_file)
        apply_all_convert(out_file)
        preview_new(out_file, TEMP_DIR)
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
        preview_orig()
        preview_new(out_file, TEMP_DIR)
        os.chdir(pwd)


def contrast_selected(event):
    """ wyór kontrastu, wywołanie przez bind """
    # global img_contrast_selected
    img_contrast_selected.set(cb_contrast.get())


def convert_contrast_button():
    """ przycisk zmiany kontrastu """
    # global file_in_path, TEMP_DIR
    out_file = pre_imagick(file_in_path.get())
    imagick(convert.convert_contrast(img_contrast.get(), img_contrast_selected.get(), e1_contrast.get(), e2_contrast.get()), out_file)
    preview_new(out_file, TEMP_DIR)


def convert_bw_button():
    """ konwersja do czerni-bieli lub sepii """
    # global file_in_path, TEMP_DIR
    out_file = pre_imagick(file_in_path.get())
    imagick(convert.convert_bw(img_bw.get(), e_bw_sepia.get()), out_file)
    preview_new(out_file, TEMP_DIR)


def convert_normalize_button():
    """ przycisk normalizacji """
    # global file_in_path, TEMP_DIR, img_normalize
    out_file = pre_imagick(file_in_path.get())
    imagick(convert.convert_normalize(img_normalize.get()), out_file)
    preview_new(out_file, TEMP_DIR)


def convert_rotate_button():
    """ przycisk obrotu """
    # global file_in_path, TEMP_DIR, img_rotate
    out_file = pre_imagick(file_in_path.get())
    imagick(convert.convert_rotate(img_rotate.get()), out_file)
    preview_new(out_file, TEMP_DIR)


def convert_resize_button():
    """ przycisk skalowania """
    # global file_in_path, TEMP_DIR, img_resize, e1_resize, e2_resize, e_border
    out_file = pre_imagick(file_in_path.get())
    imagick(convert.convert_resize(img_resize.get(), e1_resize.get(), e2_resize.get(), '0'), out_file) # ramka 0, tylko skalowanie
    preview_new(out_file, TEMP_DIR)


def convert_crop_button():
    """ przycisk wycinka """
    # global file_in_path, TEMP_DIR, img_crop, img_crop_gravity
    out_file = pre_imagick(file_in_path.get())
    imagick(convert.convert_crop(img_crop.get(), img_crop_gravity.get(), convert_crop_entries()), out_file)
    preview_new(out_file, TEMP_DIR)


def convert_crop_entries():
    """ słownik ze zmiennymi dla funkcji convert_crop """
    dict_return = {}
    dict_return['one_x1'] = e1_crop_1.get()
    dict_return['one_y1'] = e2_crop_1.get()
    dict_return['one_x2'] = e3_crop_1.get()
    dict_return['one_y2'] = e4_crop_1.get()
    dict_return['two_x1'] = e1_crop_2.get()
    dict_return['two_y1'] = e2_crop_2.get()
    dict_return['two_X'] = e3_crop_2.get()
    dict_return['two_Y'] = e4_crop_2.get()
    dict_return['three_dx'] = e1_crop_3.get()
    dict_return['three_dy'] = e2_crop_3.get()
    dict_return['three_X'] = e3_crop_3.get()
    dict_return['three_Y'] = e4_crop_3.get()
    return dict_return


def convert_text_entries():
    """ słownik ze zmiennymi dla funkcji convert_text """
    dict_return = {}
    dict_return['text_convert'] = img_text.get()
    dict_return['text'] = e_text.get()
    dict_return['dx'] = e_text_x.get()
    dict_return['dy'] = e_text_y.get()
    dict_return['gravitation'] = img_text_gravity.get()
    dict_return['font'] = img_text_font.get()
    dict_return['font_size'] = e_text_size.get()
    dict_return['text_color'] = img_text_color.get()
    dict_return['box'] = img_text_box.get()
    dict_return['box_color'] = img_text_box_color.get()
    return dict_return


def convert_text_button():
    """ przycisk wstawiania tekstu """
    # global file_in_path, TEMP_DIR
    out_file = pre_imagick(file_in_path.get())
    imagick(convert.convert_text(convert_text_entries()), out_file)
    preview_new(out_file, TEMP_DIR)


def fonts():
    """ import nazw fontów dla imagemagicka """
    # global TEMP_DIR

    if os.path.isdir(TEMP_DIR) is False:
        try:
            # print("Zakladam katalog na pliki tymczasowe: " + TEMP_DIR)
            os.mkdir(TEMP_DIR)
        except:
            # print("Nie można utworzyć katalogu na pliki tymczasowe")
            return

    if platform.system() == "Windows":
        fonts_list = ('Arial')
    else:
        file_font = os.path.join(TEMP_DIR, "fonts_list")

        command = "convert -list font > " + common.spacja(file_font)
        print(command)
        try:
            os.system(command)
        except:
            print("! Error in fonts: " + command)
            return

        try:
            file = open(file_font, "r")
            fonts_list = []
            for line in file:
                if re.search("Font", line) is not None:
                    line = re.sub('^[ ]+Font:[ ]*', "", line)
                    line = re.sub('\n', "", line)
                    fonts_list.append(line)
            file.close()
            os.remove(file_font)
        except:
            print("! Error in fonts: przy wczytywaniu listy fontów")
            fonts_list = ('Helvetica')

    cb_text_font['values'] = fonts_list


def font_selected(event):
    """ wywołanie przez bind wyboru fontu """
    # global img_text_font
    print('You selected:', cb_text_font.get())
    img_text_font.set(cb_text_font.get())


def crop_read():
    """ Wczytanie rozmiarów z obrazka do wycinka """
    # global file_in_path, img_crop_gravity
    img = Image.open(file_in_path.get())
    width = img.size[0]
    height = img.size[1]
    e1_crop_1.delete(0, "end")
    e1_crop_1.insert(0, "0")
    e2_crop_1.delete(0, "end")
    e2_crop_1.insert(0, "0")
    e3_crop_1.delete(0, "end")
    e3_crop_1.insert(0, width)
    e4_crop_1.delete(0, "end")
    e4_crop_1.insert(0, height)
    e1_crop_2.delete(0, "end")
    e1_crop_2.insert(0, "0")
    e2_crop_2.delete(0, "end")
    e2_crop_2.insert(0, "0")
    e3_crop_2.delete(0, "end")
    e3_crop_2.insert(0, width)
    e4_crop_2.delete(0, "end")
    e4_crop_2.insert(0, height)
    e1_crop_3.delete(0, "end")
    e1_crop_3.insert(0, "0")
    e2_crop_3.delete(0, "end")
    e2_crop_3.insert(0, "0")
    e3_crop_3.delete(0, "end")
    e3_crop_3.insert(0, width)
    e4_crop_3.delete(0, "end")
    e4_crop_3.insert(0, height)
    img_crop_gravity.set("C")


def open_file():
    """ otwarcie pliku obrazka do edycji """
    # global file_in_path, dir_in_path
    file_in_path.set(filedialog.askopenfilename(title=_("Select picture for processing"),
                                                initialdir=dir_in_path.get(),
                                                filetypes=(("jpeg files", "*.jpg"),
                                                           ("JPEG files", "*.JPG"),
                                                           ("all files", "*.*"))))
    file_select_L.configure(text=os.path.basename(file_in_path.get()))
    preview_orig()

    dir_in_path.set(os.path.dirname(file_in_path.get()))


def open_file_last():
    """ otwarcie ostatniego pliku """
    # global file_in_path, dir_in_path
    pwd = os.getcwd()
    os.chdir(os.path.dirname(file_in_path.get()))
    file_list = []
    for file in glob.glob("*.[j|J][p|P][g|G]"):
        file_list.append(file)
    file_list.sort()
    position = file_list.index(os.path.basename(file_in_path.get()))
    print(position, file_list)
    try:
        file = file_list[-1]
        file_select_L.configure(text=file)
        file_in_path.set(os.path.join(dir_in_path.get(), file))
        preview_orig()
    except:
        print("Error in open_file_last")
    os.chdir(pwd)


def open_file_next():
    """ otwarcie następnego pliku """
    # global file_in_path, dir_in_path
    pwd = os.getcwd()
    os.chdir(os.path.dirname(file_in_path.get()))
    file_list = []
    for file in glob.glob("*.[j|J][p|P][g|G]"):
        file_list.append(file)
    file_list.sort()
    position = file_list.index(os.path.basename(file_in_path.get()))
    print(position, file_list)
    if position <= len(file_list) - 2:
        file = file_list[position + 1]
        file_select_L.configure(text=file)
        file_in_path.set(os.path.join(dir_in_path.get(), file))
        preview_orig()
    os.chdir(pwd)


def open_file_first():
    """ otwarcie pierwszego pliku """
    # global file_in_path, dir_in_path

    pwd = os.getcwd()
    os.chdir(os.path.dirname(file_in_path.get()))
    file_list = []
    for file in glob.glob("*.[j|J][p|P][g|G]"):
        file_list.append(file)
    file_list.sort()
    position = file_list.index(os.path.basename(file_in_path.get()))
    print(position, file_list)
    try:
        file = file_list[0]
        file_select_L.configure(text=file)
        file_in_path.set(os.path.join(dir_in_path.get(), file))
        preview_orig()
    except:
        print("Error in open_file_first")
    os.chdir(pwd)


def open_file_prev():
    """ otwarcie poprzedniego pliku """
    # global file_in_path, dir_in_path

    pwd = os.getcwd()
    os.chdir(os.path.dirname(file_in_path.get()))
    file_list = []
    for file in glob.glob("*.[j|J][p|P][g|G]"):
        file_list.append(file)
    file_list.sort()
    position = file_list.index(os.path.basename(file_in_path.get()))
    print(position, file_list)
    if position > 0:
        file = file_list[position - 1]
        file_select_L.configure(text=file)
        file_in_path.set(os.path.join(dir_in_path.get(), file))
        preview_orig()
    os.chdir(pwd)


def convert_border_button():
    """ przycisk dodania ramki """
    # global file_in_path, TEMP_DIR
    out_file = pre_imagick(file_in_path.get())
    imagick(convert.convert_border(e_border.get(), img_border_color.get()), out_file)
    preview_new(out_file, TEMP_DIR)


def color_choose_border():
    """ Wybór koloru tła """
    # global img_border_color
    color = askcolor(img_border_color.get())
    if color[1] is None:
        img_border_color.set("#000000")
    else:
        img_border_color.set(color[1])
        l_border.configure(bg=img_border_color.get())


def color_choose_box_active():
    """ dodanie tła do tekstu """
    # global img_text_box
    if img_text_box.get() == 0:
        l_text_font_selected.configure(bg="#000000")
    else:
        l_text_font_selected.configure(bg=img_text_box_color.get())


def color_choose_box():
    """ Wybór koloru tła """
    # global img_text_box, img_text_box_color
    if img_text_box.get() != 0:
        color = askcolor(img_text_color.get(), root)
        if color[1] is None:
            img_text_box_color.set("#FFFFFF")
        else:
            img_text_box_color.set(color[1])
            l_text_font_selected.configure(bg=img_text_box_color.get())


def color_choose():
    """ Wybór koloru """
    # global img_text_color
    color = askcolor(img_text_color.get(), root)
    if color[1] is None:
        img_text_color.set("#FFFFFF")
    else:
        img_text_color.set(color[1])
    l_text_font_selected.configure(fg=img_text_color.get())


def ini_read_wraper():
    """ odczyt pliku ini """

    ini_entries = ini_read.ini_read(FILE_INI)
    file_in_path.set(ini_entries['file_in_path'])
    file_dir_selector.set(ini_entries['file_dir_selector'])
    work_dir.set(ini_entries['work_dir'])
    img_histograms.set(ini_entries['img_histograms'])

    ini_entries = ini_read.ini_read_resize(FILE_INI)
    img_resize.set(ini_entries['img_resize'])
    e1_resize.delete(0, "end")
    e1_resize.insert(0, ini_entries['resize_size_pixel'])
    e2_resize.delete(0, "end")
    e2_resize.insert(0, ini_entries['resize_size_percent'])

    ini_entries = ini_read.ini_read_text(FILE_INI)
    img_text.set(ini_entries['img_text'])
    img_text_font.set(ini_entries['text_font'])
    img_text_color.set(ini_entries['text_color'])
    img_text_gravity.set(ini_entries['img_text_gravity'])
    img_text_box.set(ini_entries['text_box'])
    img_text_box_color.set(ini_entries['text_box_color'])
    e_text.delete(0, "end")
    e_text.insert(0, ini_entries['text_text'])
    e_text_size.delete(0, "end")
    e_text_size.insert(0, ini_entries['text_size'])
    e_text_x.delete(0, "end")
    e_text_x.insert(0, ini_entries['text_x'])
    e_text_y.delete(0, "end")
    e_text_y.insert(0, ini_entries['text_y'])
    l_text_font_selected.configure(fg=ini_entries['text_color'])
    l_text_font_selected.configure(bg=ini_entries['text_box_color'])

    ini_entries = ini_read.ini_read_rotate(FILE_INI)
    img_rotate.set(ini_entries['img_rotate'])

    ini_entries = ini_read.ini_read_crop(FILE_INI)
    img_crop.set(ini_entries['img_crop'])
    img_crop_gravity.set(ini_entries['img_crop_gravity'])
    e1_crop_1.delete(0, "end")
    e1_crop_1.insert(0, ini_entries['crop_1_x1'])
    e2_crop_1.delete(0, "end")
    e2_crop_1.insert(0, ini_entries['crop_1_y1'])
    e3_crop_1.delete(0, "end")
    e3_crop_1.insert(0, ini_entries['crop_1_x2'])
    e4_crop_1.delete(0, "end")
    e4_crop_1.insert(0, ini_entries['crop_1_y2'])
    e1_crop_2.delete(0, "end")
    e1_crop_2.insert(0, ini_entries['crop_2_x1'])
    e2_crop_2.delete(0, "end")
    e2_crop_2.insert(0, ini_entries['crop_2_y1'])
    e3_crop_2.delete(0, "end")
    e3_crop_2.insert(0, ini_entries['crop_2_width'])
    e4_crop_2.delete(0, "end")
    e4_crop_2.insert(0, ini_entries['crop_2_height'])
    e1_crop_3.delete(0, "end")
    e1_crop_3.insert(0, ini_entries['crop_3_dx'])
    e2_crop_3.delete(0, "end")
    e2_crop_3.insert(0, ini_entries['crop_3_dy'])
    e3_crop_3.delete(0, "end")
    e3_crop_3.insert(0, ini_entries['crop_3_width'])
    e4_crop_3.delete(0, "end")
    e4_crop_3.insert(0, ini_entries['crop_3_height'])

    ini_entries = ini_read.ini_read_border(FILE_INI)
    img_border_color.set(ini_entries['img_border_color'])
    l_border.configure(bg=ini_entries['img_border_color'])
    e_border.delete(0, "end")
    e_border.insert(0, ini_entries['img_border_size'])

    ini_entries = ini_read.ini_read_color(FILE_INI)
    img_normalize.set(ini_entries['normalize'])
    img_bw.set(ini_entries['black_white'])
    e_bw_sepia.delete(0, "end")
    e_bw_sepia.insert(0, ini_entries['sepia'])

    ini_entries = ini_read.ini_read_contrast(FILE_INI)
    img_contrast.set(ini_entries['contrast'])
    e1_contrast.delete(0, "end")
    e1_contrast.insert(0, ini_entries['contrast_stretch_1'])
    e2_contrast.delete(0, "end")
    e2_contrast.insert(0, ini_entries['contrast_stretch_2'])


def ini_save():
    """ Zapis konfiguracji do pliku INI """

    # przygotowanie zawartości
    config = configparser.ConfigParser()
    config.add_section('Konfiguracja')
    config.set('Konfiguracja', 'path', file_in_path.get())
    config.set('Konfiguracja', 'work_dir', work_dir.get())
    config.set('Konfiguracja', 'file_dir', str(file_dir_selector.get()))
    config.set('Konfiguracja', 'histograms', str(img_histograms.get()))
    config.add_section('Resize')
    config.set('Resize', 'resize', str(img_resize.get()))
    config.set('Resize', 'size_pixel', e1_resize.get())
    config.set('Resize', 'size_percent', e2_resize.get())
    config.add_section('Text')
    config.set('Text', 'on', str(img_text.get()))
    config.set('Text', 'text', e_text.get())
    config.set('Text', 'gravity', img_text_gravity.get())
    config.set('Text', 'font', img_text_font.get())
    config.set('Text', 'size', e_text_size.get())
    config.set('Text', 'color', img_text_color.get())
    config.set('Text', 'box', str(img_text_box.get()))
    config.set('Text', 'box_color', img_text_box_color.get())
    config.set('Text', 'x', e_text_x.get())
    config.set('Text', 'y', e_text_y.get())
    config.add_section('Rotate')
    config.set('Rotate', 'rotate', str(img_rotate.get()))
    config.add_section('Crop')
    config.set('Crop', 'crop', str(img_crop.get()))
    config.set('Crop', '1_x1', e1_crop_1.get())
    config.set('Crop', '1_y1', e2_crop_1.get())
    config.set('Crop', '1_x2', e3_crop_1.get())
    config.set('Crop', '1_y2', e4_crop_1.get())
    config.set('Crop', '2_x1', e1_crop_2.get())
    config.set('Crop', '2_y1', e2_crop_2.get())
    config.set('Crop', '2_width', e3_crop_2.get())
    config.set('Crop', '2_height', e4_crop_2.get())
    config.set('Crop', '3_dx', e1_crop_3.get())
    config.set('Crop', '3_dy', e2_crop_3.get())
    config.set('Crop', '3_width', e3_crop_3.get())
    config.set('Crop', '3_height', e4_crop_3.get())
    config.set('Crop', 'gravity', img_crop_gravity.get())
    config.add_section('Border')
    config.set('Border', 'color', img_border_color.get())
    config.set('Border', 'size', e_border.get())
    config.add_section('Color')
    config.set('Color', 'normalize', str(img_normalize.get()))
    config.set('Color', 'black-white', str(img_bw.get()))
    config.set('Color', 'sepia', e_bw_sepia.get())
    config.add_section('Contrast')
    config.set('Contrast', 'contrast', str(img_contrast.get()))
    config.set('Contrast', 'contrast_stretch_1', e1_contrast.get())
    config.set('Contrast', 'contrast_stretch_2', e2_contrast.get())

    # save to a file
    try:
        with open(FILE_INI, 'w', encoding='utf-8', buffering=1) as configfile:
            config.write(configfile)
    except:
        print("! Error in ini_save: nie udał się zapis do pliku konfiguracyjnego: " + FILE_INI)


def help_info(event):
    """ okno info """
    # global PWD
    try:
        license_file = os.path.join(PWD, "LICENSE")
        file = open(license_file, "r", encoding="utf8")

        message = ""
        for i in file:
            message = message + i
        # file.close
    except:
        print("! Error in help_info: błąd przy wczytywaniu pliku licencji")
        message = "Copyright 2019 Tomasz Łuczak under MIT license"

    messagebox.showinfo(title=_("License"), message=message)


def close_window():
    """ zamknięcie programu """
    root.quit()
    root.destroy()
    sys.exit()


def win_deleted():
    """ zamknięcie okna programu """
    print("closed")
    close_window()


def mouse_crop_calculation(x_preview, y_preview):
    """ przeliczenie pikseli podglądu  na piksele oryginału """
    # global file_in_path
    img = Image.open(file_in_path.get())
    x_orig = img.size[0]
    y_orig = img.size[1]
    # img.close

    # x_max, y_max - wymiary podglądu, znamy max czyli PREVIEW
    if x_orig > y_orig:
        # piksele podglądu, trzeba przeliczyć y_max podglądu
        x_max = PREVIEW
        y_max = x_max*y_orig/x_orig
    elif y_orig > x_orig:
        # przeliczenie x
        y_max = PREVIEW
        x_max = y_max*x_orig/y_orig
    elif y_orig == x_orig:
        x_max = PREVIEW
        y_max = PREVIEW

    width = int(x_preview*x_orig/x_max)
    height = int(y_preview*y_orig/y_max)
    return width, height


def mouse_crop_NW(event):
    """ lewy górny narożnik """
    x_preview = event.x
    y_preview = event.y
    print("SE preview:", x_preview, y_preview)
    xy = mouse_crop_calculation(x_preview, y_preview)
    e1_crop_1.delete(0, "end")
    e1_crop_1.insert(0, xy[0])
    e2_crop_1.delete(0, "end")
    e2_crop_1.insert(0, xy[1])


def mouse_crop_SE(event):
    """ prawy dolny narożnik """
    x_preview = event.x
    y_preview = event.y
    print("NW preview:", x_preview, y_preview)
    xy = mouse_crop_calculation(x_preview, y_preview)
    e3_crop_1.delete(0, "end")
    e3_crop_1.insert(0, xy[0])
    e4_crop_1.delete(0, "end")
    e4_crop_1.insert(0, xy[1])

def preview_orig():
    """
    generowanie podglądu oryginału
    rysuje wycinek na rysunku podglądu o ile potrzeba
    """
    # global file_in_path, TEMP_DIR, img_crop, img_text_box_color, img_histograms

    if img_crop.get() == 1:
        x0 = int(e1_crop_1.get())
        y0 = int(e2_crop_1.get())
        x1 = int(e3_crop_1.get())
        y1 = int(e4_crop_1.get())
        do_nothing = 0
    elif img_crop.get() == 2:
        x0 = int(e1_crop_2.get())
        y0 = int(e2_crop_2.get())
        x1 = x0 + int(e3_crop_2.get())
        y1 = y0 + int(e4_crop_2.get())
        do_nothing = 0
    else:
        do_nothing = 1

    if do_nothing != 1:
        im = Image.open(file_in_path.get())
        x_orig = im.size[0]
        y_orig = im.size[1]

        # x_max, y_max - wymiary podglądu, znamy max czyli PREVIEW
        if x_orig > y_orig:
            # piksele podglądu, trzeba przeliczyć y_max podglądu
            x_max = PREVIEW
            y_max = x_max*y_orig/x_orig
        elif y_orig > x_orig:
            # przeliczenie x
            y_max = PREVIEW
            x_max = y_max*x_orig/y_orig
        elif y_orig == x_orig:
            x_max = PREVIEW
            y_max = PREVIEW

        ratio_X = x_max / int(x_orig)
        ratio_Y = y_max / int(y_orig)
        x0 = int(x0 * ratio_X)
        y0 = int(y0 * ratio_Y)
        x1 = int(x1 * ratio_X)
        y1 = int(y1 * ratio_Y)

        x0y0x1y1 = str(x0) + "," + str(y0) + " " + str(x1) + "," + str(y1)
        command = " -fill none  -draw \"stroke '#FFFF00' rectangle " + x0y0x1y1 + "\" "
    else:
        command = " "

    preview = convert_preview(file_in_path.get(), TEMP_DIR, command)
    try:
        pi_preview_orig.configure(file=common.spacja(preview['filename']))
        l_preview_orig.configure(text=preview['width'] + "x" + preview['height'])
    except:
        print("! Error in preview_orig: Nie można wczytać podglądu")

    if img_histograms.get() == 1:
        try:
            pi_histogram_orig.configure(file=preview_histogram(file_in_path.get()))
        except:
            print("! Error in preview_orig: : Nie można wczytać podglądu histogramu")
    else:
        print("Bez podglądu histogramu")



def tools_set():
    """ wybór narzędzi do wyświetlenia """

    if img_resize.get() == 0:
        frame_resize.grid_remove()
    else:
        frame_resize.grid()

    if img_crop.get() == 0:
        frame_crop.grid_remove()
    else:
        frame_crop.grid()

    if img_text.get() == 0:
        frame_text.grid_remove()
    else:
        frame_text.grid()

    if img_rotate.get() == 0:
        frame_rotate.grid_remove()
    else:
        frame_rotate.grid()

    if img_border.get() == 0:
        frame_border.grid_remove()
    else:
        frame_border.grid()

    if img_bw.get() == 0:
        frame_bw.grid_remove()
    else:
        frame_bw.grid()

    if img_normalize.get() == 0:
        frame_normalize.grid_remove()
    else:
        frame_normalize.grid()

    if img_contrast.get() == 0:
        frame_contrast.grid_remove()
    else:
        frame_contrast.grid()

    if img_histograms.get() == 0:
        frame_histogram_orig.grid_remove()
        frame_histogram_new.grid_remove()
    else:
        frame_histogram_orig.grid()
        frame_histogram_new.grid()

###############################################################################
# GUI okno główne
###############################################################################

root = Tk()

# hidden file
# https://code.activestate.com/lists/python-tkinter-discuss/3723/
try:
    # call a dummy dialog with an impossible option to initialize the file
    # dialog without really getting a dialog window; this will throw a
    # TclError, so we need a try...except :
    try:
        root.tk.call('tk_getOpenFile', '-foobarbaz')
    except TclError:
        pass
    # now set the magic variables accordingly
    root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
    root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
except:
    pass

root.title("Tomasz Łuczak : FotoKilof : " + str(VERSION) + " : " +
           str(datetime.date.today()))

style = ttk.Style()

if platform.system() != "Windows":
    style.theme_use('clam')

style.configure("Blue.TButton", foreground="blue")
style.configure("Blue.TLabelframe.Label", foreground="blue")

##########################
# Zmienne globalne

FILE_INI = "fotokilof.ini"
PWD = os.getcwd()
TEMP_DIR = os.path.join(PWD, "tmp")
work_dir = StringVar()  # default: "FotoKilof"
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
img_border = IntVar()
img_border_color = StringVar()
img_normalize = IntVar()
img_bw = IntVar()
img_contrast = IntVar()
img_contrast_selected = StringVar()
img_histograms = IntVar()

######################################################################
# Karty
######################################################################
main = ttk.Frame(root)
main.pack()

####################################################################
# Kolumna menu
####################################################################
frame_zero_col = ttk.Frame(main)
frame_zero_col.grid(row=1, column=1, rowspan=2, sticky=(N, W, E, S))
###########################
# Wybór poleceń
###########################
frame_zero_set = ttk.Labelframe(frame_zero_col, text=_("Tools"),
                                style="Blue.TLabelframe")
frame_zero_set.grid(row=1, column=1, padx=5, pady=5, sticky=(W, E))

cb_histograms = ttk.Checkbutton(frame_zero_set, text=_("Histograms"),
                                variable=img_histograms,
                                offvalue="0", onvalue="1")
cb_resize = ttk.Checkbutton(frame_zero_set, text=_("Scaling/Resize"),
                            variable=img_resize, offvalue="0", onvalue="1")
cb_crop = ttk.Checkbutton(frame_zero_set, text=_("Crop"), variable=img_crop,
                          offvalue="0", onvalue="1")
cb_text = ttk.Checkbutton(frame_zero_set, text=_("Text"), variable=img_text,
                          onvalue="1", offvalue="0")
cb_rotate = ttk.Checkbutton(frame_zero_set, text=_("Rotate"),
                            variable=img_rotate, offvalue="0", onvalue="90")
cb_border = ttk.Checkbutton(frame_zero_set, text=_("Frame"),
                            variable=img_border, offvalue="0", onvalue="1")
cb_bw = ttk.Checkbutton(frame_zero_set, text=_("Black&white"),
                        variable=img_bw, offvalue="0", onvalue="1")
cb_normalize = ttk.Checkbutton(frame_zero_set, text=_("Colors normalize"),
                               variable=img_normalize, offvalue="0", onvalue="1")
cb_contrast = ttk.Checkbutton(frame_zero_set, text=_("Contrast"),
                              variable=img_contrast, offvalue="0", onvalue="1")

b_last_set = ttk.Button(frame_zero_set, text=_("Apply"), command=tools_set)

cb_histograms.pack(padx=5, pady=5, anchor=W)
cb_resize.pack(padx=5, pady=5, anchor=W)
cb_crop.pack(padx=5, pady=5, anchor=W)
cb_text.pack(padx=5, pady=5, anchor=W)
cb_rotate.pack(padx=5, pady=5, anchor=W)
cb_border.pack(padx=5, pady=5, anchor=W)
cb_bw.pack(padx=5, pady=5, anchor=W)
cb_normalize.pack(padx=5, pady=5, anchor=W)
cb_contrast.pack(padx=5, pady=5, anchor=W)

b_last_set.pack(padx=5, pady=5)
###########################
# Przyciski
###########################
frame_zero_cmd = ttk.Labelframe(frame_zero_col, text=_("Commands"),
                                style="Blue.TLabelframe")
frame_zero_cmd.grid(row=2, column=1, padx=5, pady=5, sticky=(W, E))

b_last_quit = ttk.Button(frame_zero_cmd, text=_("Exit"),
                         command=close_window)
b_last_save = ttk.Button(frame_zero_cmd, text=_("Save settings"),
                         command=ini_save)
b_last_read = ttk.Button(frame_zero_cmd, text=_("Load settings"),
                         command=ini_read_wraper)
b_last_apply = ttk.Button(frame_zero_cmd, text=_("Apply all"),
                          command=apply_all, style="Blue.TButton")

b_last_apply.pack(padx=5, pady=25, anchor=W)
b_last_save.pack(padx=5, pady=5, anchor=W)
b_last_read.pack(padx=5, pady=5, anchor=W)
b_last_quit.pack(padx=5, pady=25, anchor=W)


#####################################################################
# Pierwsza kolumna
#####################################################################
frame_first_col = ttk.Frame(main)
frame_first_col.grid(row=1, column=2, rowspan=2, sticky=(N, W, E, S))

###########################
# Wybór obrazka
###########################
frame_input = ttk.Labelframe(frame_first_col, text=_("Image"),
                             style="Blue.TLabelframe")
frame_input.grid(row=1, column=1, columnspan=2, sticky=(N, W, E, S),
                 padx=5, pady=5)
# tworzenie widgetów
# l_select_what = ttk.Label(frame_input, text=_("Processed:")
b_file_select = ttk.Button(frame_input, text=_("File selection"),
                           command=open_file, style="Blue.TButton")
rb_selector_dir = ttk.Radiobutton(frame_input, text=_("Folder"),
                                  variable=file_dir_selector, value="1")
rb_selector_file = ttk.Radiobutton(frame_input, text=_("File"),
                                   variable=file_dir_selector, value="0")
file_select_L = ttk.Label(frame_input, width=24)


b_file_select_first = ttk.Button(frame_input, text=_("First"),
                                 command=open_file_first)
b_file_select_prev = ttk.Button(frame_input, text=_("Previous"),
                                command=open_file_prev)
b_file_select_next = ttk.Button(frame_input, text=_("Next"),
                                command=open_file_next)
b_file_select_last = ttk.Button(frame_input, text=_("Last"),
                                command=open_file_last)
# umieszczenie widgetów
# l_select_what.grid(column=1, row=1, padx=5, pady=5, sticky=W)
b_file_select.grid(column=1, row=1, padx=5, pady=5, sticky=W)
rb_selector_dir.grid(column=2, row=1, padx=5, pady=5, sticky=W)
rb_selector_file.grid(column=3, row=1, padx=5, pady=5, sticky=W)
file_select_L.grid(column=4, row=1, padx=5, pady=5, sticky=W, columnspan=2)
#
b_file_select_first.grid(column=1, row=2, padx=5, pady=5, sticky=W)
b_file_select_prev.grid(column=2, row=2, padx=5, pady=5, sticky=W, columnspan=2)
b_file_select_next.grid(column=4, row=2, padx=5, pady=5, sticky=W)
b_file_select_last.grid(column=5, row=2, padx=5, pady=5, sticky=W)

###########################
# Resize
###########################
frame_resize = ttk.Labelframe(frame_first_col, text=_("Scale/Resize"),
                              style="Blue.TLabelframe")
frame_resize.grid(column=1, row=2, columnspan=2, sticky=(N, W, E, S),
                  padx=5, pady=5)
###
rb_1_resize = ttk.Radiobutton(frame_resize, text=_("Pixels"),
                              variable=img_resize, value="1")
e1_resize = ttk.Entry(frame_resize, width=7)
rb_2_resize = ttk.Radiobutton(frame_resize, text=_("Percent"),
                              variable=img_resize, value="2")
e2_resize = ttk.Entry(frame_resize, width=7)
rb_3_resize = ttk.Radiobutton(frame_resize, text="FullHD (1920x1080)",
                              variable=img_resize, value="3")
rb_4_resize = ttk.Radiobutton(frame_resize, text="2K (2048×1556)",
                              variable=img_resize, value="4")
rb_5_resize = ttk.Radiobutton(frame_resize, text="4K (4096×3112)",
                              variable=img_resize, value="5")
b_resize = ttk.Button(frame_resize, text=_("Resize"), style="Blue.TButton",
                      command=convert_resize_button)

rb_3_resize.grid(row=1, column=1, columnspan=2, sticky=W, padx=5, pady=5)
rb_4_resize.grid(row=1, column=3, columnspan=2, sticky=W, padx=5, pady=5)
rb_5_resize.grid(row=1, column=5, columnspan=2, sticky=W, padx=5, pady=5)
rb_1_resize.grid(row=2, column=1, sticky=W, padx=5, pady=5)
e1_resize.grid(row=2, column=2, sticky=W, padx=5, pady=5)
rb_2_resize.grid(row=2, column=3, sticky=W, padx=5, pady=5)
e2_resize.grid(row=2, column=4, sticky=W, padx=5, pady=5)
b_resize.grid(row=2, column=6, sticky=(E), padx=5, pady=5)

############################
# crop
############################
frame_crop = ttk.Labelframe(frame_first_col, text=_("Crop"),
                            style="Blue.TLabelframe")
frame_crop.grid(row=3, column=1, columnspan=2, sticky=(N, W, E, S),
                padx=5, pady=5)
###
rb0_crop = ttk.Radiobutton(frame_crop, text=_("None"), variable=img_crop, value="0")
rb1_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="1",
                           text=_("Coordinates (x1, y1) and (x2, y2)"))
f_clickL_crop = ttk.Labelframe(frame_crop, text=_("Left Upper corner"))
l_clickL_crop = ttk.Label(f_clickL_crop, text=_("Click left"))
e1_crop_1 = ttk.Entry(f_clickL_crop, width=4)
e2_crop_1 = ttk.Entry(f_clickL_crop, width=4)
f_clickR_crop = ttk.Labelframe(frame_crop, text=_("Right lower corner"))
l_clickR_crop = ttk.Label(f_clickR_crop, text=_("Click right"))
e3_crop_1 = ttk.Entry(f_clickR_crop, width=4)
e4_crop_1 = ttk.Entry(f_clickR_crop, width=4)

rb2_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="2",
                           text=_("Origin (x1,y1) and dimensions (X, Y)"))
e1_crop_2 = ttk.Entry(frame_crop, width=4)
e2_crop_2 = ttk.Entry(frame_crop, width=4)
e3_crop_2 = ttk.Entry(frame_crop, width=4)
e4_crop_2 = ttk.Entry(frame_crop, width=4)

rb3_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="3",
                           text=_("Offset (dx,dy), dimensions (X, Y)\ni gravity"))
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

b_crop_read = ttk.Button(frame_crop, text=_("Load coordinates from image"),
                         command=crop_read)
b_crop = ttk.Button(frame_crop, text=_("Crop"), style="Blue.TButton",
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
rbN_crop_3.grid(row=1, column=2, pady=5)
rbNE_crop_3.grid(row=1, column=3, sticky=W, pady=5)
rbW_crop_3.grid(row=2, column=1, sticky=W, pady=5)
rbC_crop_3.grid(row=2, column=2, sticky=W, pady=5)
rbE_crop_3.grid(row=2, column=3, sticky=W, pady=5)
rbSW_crop_3.grid(row=3, column=1, sticky=W, pady=5)
rbS_crop_3.grid(row=3, column=2, pady=5)
rbSE_crop_3.grid(row=3, column=3, sticky=W, pady=5)
b_crop_read.grid(row=5, column=2, columnspan=4, sticky=W, padx=5, pady=5)
b_crop.grid(row=5, column=1, sticky=W, padx=5, pady=5)

###########################
# Tekst
###########################
frame_text = ttk.Labelframe(frame_first_col, text=_("Add text"),
                            style="Blue.TLabelframe")
frame_text.grid(row=4, column=1, columnspan=2, sticky=(N, W, E, S),
                padx=5, pady=5)
###
frame_text_text = ttk.Frame(frame_text)

e_text = ttk.Entry(frame_text_text, width=65)
frame_text_text.grid(row=1, column=1, columnspan=5, sticky=(W, E))
e_text.grid(row=1, column=2, sticky=W, padx=5)
###
frame_text_xy = ttk.Frame(frame_text)
l_text_xy = ttk.Label(frame_text_xy, text=_("Offset (dx,dy)\n"))
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
rbN.grid(row=1, column=2, pady=5)
rbNE.grid(row=1, column=3, sticky=W, pady=5)
rbW.grid(row=2, column=1, sticky=W, pady=5)
rbC.grid(row=2, column=2, pady=5)
rbE.grid(row=2, column=3, sticky=W, pady=5)
rbSW.grid(row=3, column=1, sticky=W, pady=5)
rbS.grid(row=3, column=2, pady=5)
rbSE.grid(row=3, column=3, sticky=W, pady=5)

###
frame_text_font = ttk.Frame(frame_text)
cb_text_font = ttk.Combobox(frame_text_font, textvariable=img_text_font)
e_text_size = ttk.Entry(frame_text_font, width=3)
b_text_color = ttk.Button(frame_text, text=_("Font color"), command=color_choose)
cb_text_box = ttk.Checkbutton(frame_text_font, text=_("Background"),
                              variable=img_text_box, onvalue="1", offvalue="0",
                              command=color_choose_box_active)
b_text_box_color = ttk.Button(frame_text, text=_("Background color"),
                              command=color_choose_box)
l_text_windows = ttk.Label(frame_text, width=40)
b_text = ttk.Button(frame_text, text=_("Put text"), style="Blue.TButton",
                    command=convert_text_button)
l_text_font_selected = Label(frame_text, width=20, textvariable=img_text_font)

l_text_font_selected.grid(row=3, column=1, sticky=(W, E), padx=5)
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
frame_rotate = ttk.Labelframe(frame_first_col, text=_("Rotate"),
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
b_rotate = ttk.Button(frame_rotate, text=_("Rotate"), style="Blue.TButton",
                      command=convert_rotate_button)

rb_rotate_0.grid(row=1, column=1, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_90.grid(row=1, column=2, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_180.grid(row=1, column=3, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_270.grid(row=1, column=4, sticky=(N, W, E, S), padx=5, pady=5)
b_rotate.grid(row=1, column=5, padx=5, pady=5)

############################
# Czarno-białe
############################
frame_bw = ttk.LabelFrame(frame_first_col, text=_("Black-white"),
                          style="Blue.TLabelframe")
frame_bw.grid(row=5, column=2, rowspan=2, sticky=(N, W, E, S), padx=5, pady=5)
###
rb1_bw = ttk.Radiobutton(frame_bw, text=_("Black-white"), variable=img_bw, value="1")
rb2_bw = ttk.Radiobutton(frame_bw, text=_("Sepia"), variable=img_bw, value="2")
e_bw_sepia = ttk.Entry(frame_bw, width=3)
l_bw_sepia = ttk.Label(frame_bw, text="%")
b_bw = ttk.Button(frame_bw, text=_("Execute"), style="Blue.TButton",
                  command=convert_bw_button)

rb1_bw.grid(row=1, column=1, padx=5, pady=5, sticky=W)
rb2_bw.grid(row=2, column=1, padx=5, pady=5, sticky=W)
e_bw_sepia.grid(row=2, column=2, padx=5, pady=5, sticky=E)
l_bw_sepia.grid(row=2, column=3, padx=5, pady=5, sticky=W)
b_bw.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=E)

###########################
# Border
###########################
frame_border = ttk.Labelframe(frame_first_col, text=_("Frame"),
                              style="Blue.TLabelframe")
frame_border.grid(row=6, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
l_border = Label(frame_border, text=_("Pixels"))
e_border = ttk.Entry(frame_border, width=3)
b1_border = ttk.Button(frame_border, text=_("Color"), command=color_choose_border)
b_border = ttk.Button(frame_border, text=_("Add frame"), style="Blue.TButton",
                      command=convert_border_button)
l_border.grid(row=1, column=1, padx=5, pady=5)
e_border.grid(row=1, column=2, padx=5, pady=5)
b1_border.grid(row=1, column=3, padx=5, pady=5)
b_border.grid(row=1, column=4, padx=5, pady=5, sticky=E)

########################################################################
# Druga kolumna
########################################################################
frame_second_col = ttk.Frame(main)
frame_second_col.grid(row=1, column=3, sticky=(N, W, E, S))

############################
# Ramka podglądu oryginału
############################
frame_preview_orig = ttk.Labelframe(frame_second_col, text=_("Original"),
                                    style="Blue.TLabelframe")
frame_preview_orig.grid(row=1, column=1, columnspan=2, sticky=(N, W, E, S),
                        padx=5, pady=5)
###
b_preview_orig = ttk.Button(frame_preview_orig, text=_("Original"),
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
frame_histogram_orig = ttk.LabelFrame(frame_second_col, text=_("Histogram"))
frame_histogram_orig.grid(row=2, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
pi_histogram_orig = PhotoImage()
l_histogram_orig = ttk.Label(frame_histogram_orig, image=pi_histogram_orig)
l_histogram_orig.grid(row=1, column=1, padx=10, pady=5)

########################
# Kontrast
#########################
frame_contrast = ttk.Labelframe(frame_second_col, text=_("Contrast"),
                                style="Blue.TLabelframe")
frame_contrast.grid(row=2, column=2, sticky=(N, W, E, S), padx=5, pady=5)
###
b_contrast = ttk.Button(frame_contrast, text=_("Contrast"), style="Blue.TButton",
                        command=convert_contrast_button)
rb1_contrast = ttk.Radiobutton(frame_contrast, text=_("Contrast"),
                               variable=img_contrast, value="1")
cb_contrast = ttk.Combobox(frame_contrast, width=2,
                           values=("+2", "+1", "0", "-1", "-2"))
rb2_contrast = ttk.Radiobutton(frame_contrast, text=_("Stretch"),
                               variable=img_contrast, value="2")
e1_contrast = ttk.Entry(frame_contrast, width=4)
e2_contrast = ttk.Entry(frame_contrast, width=4)
l1_contrast = ttk.Label(frame_contrast, text=_("Black"))
l2_contrast = ttk.Label(frame_contrast, text=_("White"))

rb1_contrast.grid(row=1, column=1, padx=5, pady=5, sticky=W)
cb_contrast.grid(row=1, column=2, padx=5, pady=5, sticky=W)
rb2_contrast.grid(row=2, column=1, padx=5, pady=5, sticky=W)
e1_contrast.grid(row=3, column=1, padx=5, pady=5, sticky=E)
e2_contrast.grid(row=3, column=2, padx=5, pady=5, sticky=W)
l1_contrast.grid(row=4, column=1, padx=5, pady=5, sticky=E)
l2_contrast.grid(row=4, column=2, padx=5, pady=5, sticky=W)
b_contrast.grid(row=5, column=1, padx=5, pady=5, columnspan=3, sticky=E)


############################
# Normalize
############################
frame_normalize = ttk.LabelFrame(frame_second_col, text=_("Color normalize"),
                                 style="Blue.TLabelframe")
frame_normalize.grid(row=3, column=1, columnspan=2, sticky=(N, W, E, S),
                     padx=5, pady=5)
###
rb1_normalize = ttk.Radiobutton(frame_normalize, text=_("Normalize"),
                                variable=img_normalize, value="1")
rb2_normalize = ttk.Radiobutton(frame_normalize, text=_("AutoLevel"),
                                variable=img_normalize, value="2")
b_normalize = ttk.Button(frame_normalize, text=_("Normalize"),
                         style="Blue.TButton",
                         command=convert_normalize_button)

rb1_normalize.grid(row=1, column=1, padx=5, pady=5, sticky=W)
rb2_normalize.grid(row=1, column=2, padx=5, pady=5, sticky=W)
b_normalize.grid(row=1, column=3, padx=5, pady=5, sticky=E)

#####################################################
# Trzecia kolumna
#####################################################
frame_third_col = ttk.Frame(main)
frame_third_col.grid(row=1, column=4, sticky=(N, W, E, S))

##########################
# Ramka podglądu wyniku
###########################
frame_preview_new = ttk.Labelframe(frame_third_col, text=_("Result"),
                                   style="Blue.TLabelframe")
frame_preview_new.grid(row=1, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
b_preview_new = ttk.Button(frame_preview_new, text=_("Result"),
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
frame_histogram_new = ttk.LabelFrame(frame_third_col, text=_("Histogram"))
frame_histogram_new.grid(row=2, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
pi_histogram_new = PhotoImage()
l_histogram_new = ttk.Label(frame_histogram_new, image=pi_histogram_new)
l_histogram_new.grid(row=1, column=1, padx=10, pady=5)

##########################
# Postęp
##########################
# l_last_progress_files = ttk.Label(frame_last, textvariable=progress_files)
# l_last_progress_filename = ttk.Label(frame_last, textvariable=progress_filename)

# l_last_progress_files.grid(row=1, column=6, padx=5)
# l_last_progress_filename.grid(row=1, column=7, padx=5)

###############################################################################
# bind
###############################################################################

# podpinanie poleceń do widgetów, menu, skrótów
cb_text_font.bind("<<ComboboxSelected>>", font_selected)
cb_contrast.bind("<<ComboboxSelected>>", contrast_selected)
l_preview_orig_pi.bind("<Button-1>", mouse_crop_NW)
l_preview_orig_pi.bind("<Button-3>", mouse_crop_SE)
rb0_crop.bind("<Button-1>", preview_orig_bind)
rb1_crop.bind("<ButtonRelease-1>", preview_orig_bind)
rb2_crop.bind("<ButtonRelease-1>", preview_orig_bind)
rb3_crop.bind("<Button-1>", preview_orig_bind)
root.bind("<F1>", help_info)
root.protocol("WM_DELETE_WINDOW", win_deleted)

###############
# Uruchomienie funkcji
#
ini_read_wraper()  # Wczytanie konfiguracji
fonts()    # Wczytanie dostępnych fontów
no_text_in_windows()  # Ostrzeżenie, jesli Windows
tools_set()
dir_in_path.set(os.path.dirname(file_in_path.get()))  # wczytanie ścieżki
if os.path.isfile(file_in_path.get()):
    # Wczytanie podglądu oryginału
    preview_orig()

l_border.configure(bg=img_border_color.get())

root.mainloop()

# EOF
