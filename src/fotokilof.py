# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" nice GUI for  ImageMagick with few common used (by me) command """

import configparser
import datetime
import gettext
import glob
import platform
import os
import re
import sys

from tkinter import Tk, ttk, Label, PhotoImage, Text
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from tkinter import TclError, StringVar, IntVar
from tkinter import N, S, W, E, END, NORMAL, DISABLED

from tkcolorpicker import askcolor
from PIL import Image

import touch

import convert
import common
import ini_read
import magick
import preview

if sys.platform.startswith('win'):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('fotokilof', localedir, fallback=True)
gettext.install('fotokilof', localedir)
_ = translate.gettext

###################
# CONSTANTS
VERSION = "2.8"
if platform.system() == "Windows":
    PREVIEW_ORIG = 400  # preview original
    PREVIEW_NEW = 400  # preview result
    PREVIEW_LOGO = 80  # preview logo
else:
    PREVIEW_ORIG = 450
    PREVIEW_NEW = 450
    PREVIEW_LOGO = 100

##########################


def no_text_in_windows():
    """ info dla Windows, że może być problem z dodaniem tekstu """
    if platform.system() == "Windows":
        l_text_windows.configure(text=_("Unfortunately, you are using Windows, thus not all option will work"))


def print_command(cmd, cmd_imagick):
    """ print command in custom window """
#    t_custom.delete(1.0, END)  # delete whole text in widget
    t_custom.insert(END, cmd + " ")

    cb_custom_command.current(imagick_commands.index(cmd_imagick))

################
# Preview


def preview_orig_bind(event):
    """ preview orginal picture via bind """
    preview_orig()


def preview_new(file_out, dir_temp):
    """ generowanie podglądu wynikowego """
    # global img_histograms_on
    preview_picture = preview.preview_convert(file_out, dir_temp, " ", PREVIEW_NEW)
    try:
        pi_preview_new.configure(file=preview_picture['filename'])
        l_preview_new.configure(text=preview_picture['width'] + "x" \
                                + preview_picture['height'])
    except:
        print("! Error in preview_new: Nie można wczytać podglądu")

    if img_histograms_on.get() == 1:
        try:
            pi_histogram_new.configure(file=preview.preview_histogram(file_out,
                                                                      TEMP_DIR))
        except:
            print("! Error in preview histogram_new")


def preview_orig_button():
    """ podgląd oryginału """
    # global file_in_path

    try:
        img = Image.open(file_in_path.get())
        img.show()
    except:
        print("No orig picture to preview")


def preview_new_button():
    """ podgląd wynikowego obrazka """

    file_show = os.path.join(os.path.dirname(file_in_path.get()),
                             work_dir.get(),
                             os.path.basename(file_in_path.get()))
    try:
        img = Image.open(file_show)
        img.show()
    except:
        print("No new picture to preview")


def apply_all_convert(out_file):
    """ apply all option together """
    text_separate = 0  # all conversion in one run
    cmd = ""

    if img_normalize_on.get() == 1:
        cmd = cmd + " " + convert.convert_normalize(img_normalize.get())

    if img_contrast_on.get() == 1:
        cmd = cmd + " " + convert.convert_contrast(img_contrast.get(),
                                                   img_contrast_selected.get(),
                                                   e1_contrast.get(),
                                                   e2_contrast.get())

    if img_bw_on.get() == 1:
        cmd = cmd + " " + convert.convert_bw(img_bw.get(), e_bw_sepia.get())

    if int(img_resize_on.get()) == 1:
        if img_border_on.get() == 0:
            border = 0
        else:
            border = abs(int(e_border.get()))
        cmd = cmd + " " + convert.convert_resize(img_resize.get(),
                                                 e1_resize.get(),
                                                 e2_resize.get(),
                                                 border)
    elif int(img_crop_on.get()) == 1:
        # if crop with mogrify, convert text in second run
        text_separate = 1
        cmd = cmd + " " + convert.convert_crop(img_crop.get(),
                                               img_crop_gravity.get(),
                                               convert_crop_entries())

    if img_rotate_on.get() > 0:
        cmd = cmd + " " + convert.convert_rotate(img_rotate.get())

    if img_border_on.get() == 1:
        border = int(e_border.get())
        cmd = cmd + " " + convert.convert_border(e_border.get(),
                                                 img_border_color.get(),
                                                 border)
    cmd_text = convert.convert_text(convert_text_entries())

    cmd_imagick = "mogrify"
    if text_separate == 0:
        cmd = cmd + " " + cmd_text
        print_command(cmd + out_file, cmd_imagick)
        result1 = magick.imagick(cmd, out_file, cmd_imagick)
        result2 = None
    else:
        # thus text gravity which makes problem with crop gravity
        # foce second run of conversion
        print_command(cmd +  out_file, cmd_imagick)
        result1 = magick.imagick(cmd, out_file, cmd_imagick)
        result2 = magick.imagick(cmd_text, out_file, cmd_imagick)

    if img_logo_on.get() == 1:
        cmd1 = convert.convert_pip(img_logo_gravity.get(),
                                   e_logo_width.get(),
                                   e_logo_height.get(),
                                   e_logo_dx.get(),
                                   e_logo_dy.get())
        cmd2 = " " + common.spacja(file_logo_path.get()) + " " \
            + common.spacja(out_file)
        cmd = cmd1 + cmd2
        cmd_imagick = "composite"
        print_command(cmd, cmd_imagick)
        result3 = magick.imagick(cmd, out_file, cmd_imagick)
    else:
        result3 = None

    if result1 == "OK" or result2 == "OK" or result3 == "OK":
        result = "OK"
    else:
        result = "None"
    return result


def apply_all_button():
    """
    zaplikowanie wszystkich opcji na raz
    mieli albo plik albo cały katalog
    """
    progress_files.set(_("Processing"))
    pb.start()
    root.update_idletasks()
    if file_dir_selector.get() == 0:
        out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
        result = apply_all_convert(out_file)
        if result == "OK":
            preview_new(out_file, TEMP_DIR)
    else:
        pwd = os.getcwd()
        os.chdir(os.path.dirname(file_in_path.get()))
        i = 0
        files_list = glob.glob("*.[j|J][p|P][g|G]")
        file_list_len = len(files_list)
        pb['maximum'] = file_list_len
        pb['mode'] = "determinate"
        for files in glob.glob("*.[j|J][p|P][g|G]"):
            out_file = magick.pre_imagick(files, work_dir.get())
            result = apply_all_convert(os.path.realpath(out_file))
            i = i + 1
            progress_files.set(str(i) + " " + _("of") + " " \
                               + str(file_list_len) + " : " + files)
            progress_var.set(i)
            root.update_idletasks()
        preview_orig()
        if result == "OK":
            preview_new(out_file, TEMP_DIR)
        os.chdir(pwd)

    progress_var.set(0)
    progress_files.set(_("done"))
    pb.stop()
    root.update_idletasks()


def convert_custom_button():
    """ execute custom command """
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = t_custom.get('1.0', 'end-1c')
    cmd_imagick = cb_custom_command.get()
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)


def contrast_selected(event):
    """ Contrast selected, called by bind """
    img_contrast_selected.set(cb_contrast.get())


def convert_contrast_button():
    """ przycisk zmiany kontrastu """
    root.update_idletasks()
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = convert.convert_contrast(img_contrast.get(),
                                   img_contrast_selected.get(),
                                   e1_contrast.get(),
                                   e2_contrast.get())
    cmd_imagick = "mogrify"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)
    progress_var.set(0)


def convert_bw_button():
    """ black-white or sepia button """
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = convert.convert_bw(img_bw.get(), e_bw_sepia.get())
    cmd_imagick = "mogrify"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)


def convert_normalize_button():
    """ normalize button """
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = convert.convert_normalize(img_normalize.get())
    cmd_imagick = "mogrify"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)


def convert_rotate_button():
    """ rotate button """
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = convert.convert_rotate(img_rotate.get())
    cmd_imagick = "mogrify"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)


def convert_resize_button():
    """ resize button """
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = convert.convert_resize(img_resize.get(),
                                 e1_resize.get(),
                                 e2_resize.get(),
                                 '0')
    cmd_imagick = "mogrify"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)


def convert_border_button():
    """ przycisk dodania ramki """
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = convert.convert_border(e_border.get(),
                                 img_border_color.get(),
                                 img_border_on.get())
    cmd_imagick = "mogrify"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)


def convert_crop_button():
    """ przycisk wycinka """
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = convert.convert_crop(img_crop.get(),
                               img_crop_gravity.get(),
                               convert_crop_entries())
    cmd_imagick = "mogrify"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)


def convert_logo_button():
    """ Button insert logo """
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd1 = convert.convert_pip(img_logo_gravity.get(),
                               e_logo_width.get(),
                               e_logo_height.get(),
                               e_logo_dx.get(),
                               e_logo_dy.get())
    cmd2 = common.spacja(file_logo_path.get()) + " " + common.spacja(out_file)
    cmd = cmd1 + " " + cmd2
    cmd_imagick = "composite"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
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
    dict_return['two_width'] = e3_crop_2.get()
    dict_return['two_height'] = e4_crop_2.get()
    dict_return['three_dx'] = e1_crop_3.get()
    dict_return['three_dy'] = e2_crop_3.get()
    dict_return['three_width'] = e3_crop_3.get()
    dict_return['three_height'] = e4_crop_3.get()
    return dict_return


def convert_text_entries():
    """ słownik ze zmiennymi dla funkcji convert_text """
    dict_return = {}
    dict_return['text_on'] = img_text_on.get()
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
    out_file = magick.pre_imagick(file_in_path.get(), work_dir.get())
    cmd = convert.convert_text(convert_text_entries())
    cmd_imagick = "mogrify"
    print_command(cmd, cmd_imagick)
    result = magick.imagick(cmd, out_file, cmd_imagick)
    if result == "OK":
        preview_new(out_file, TEMP_DIR)


def fonts():
    """ import nazw fontów dla imagemagicka """

    if os.path.isdir(TEMP_DIR) is False:
        try:
            os.mkdir(TEMP_DIR)
        except:
            # print("Nie można utworzyć katalogu na pliki tymczasowe")
            return

    file_font = os.path.normpath(os.path.join(TEMP_DIR, "fonts_list"))

    touch.touch(file_font)
    command = "-list font > "
    magick.imagick(command, common.spacja(file_font), "convert")

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
    # print('You selected:', cb_text_font.get())
    img_text_font.set(cb_text_font.get())


def crop_read():
    """ Wczytanie rozmiarów z obrazka do wycinka """
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


def open_file_logo():
    """ open logo file for inserting """
    directory = os.path.dirname(file_logo_path.get())
    filetypes = ((_("jpeg files"), "*.jpg"),
                 (_("JPEG files"), "*.JPG"),
                 (_("png files"), "*.png"),
                 (_("PNG files"), "*.PNG"),
                 (_("All files"), "*.*"))
    file_logo_path.set(filedialog.askopenfilename(title=_("Select logo picture for inserting"),
                                                  initialdir=directory,
                                                  filetypes=filetypes))

    preview_logo()


def open_file():
    """ open image for processing """
    directory = os.path.dirname(file_in_path.get())
    filetypes = ((_("jpeg files"), "*.jpg"),
                 (_("JPEG files"), "*.JPG"),
                 (_("png files"), "*.png"),
                 (_("PNG files"), "*.PNG"),
                 (_("All files"), "*.*"))
    file_in_path.set(filedialog.askopenfilename(title=_("Select picture for processing"),
                                                initialdir=directory,
                                                filetypes=filetypes))
    file_select_L.configure(text=os.path.basename(file_in_path.get()))
    preview_orig()


def open_file_last():
    """ Open last file """
    if file_in_path.get():
        if os.path.isfile(file_in_path.get()):
            cwd = os.path.dirname(file_in_path.get())
            file_list = common.list_of_images(cwd)
            current_file = os.path.basename(file_in_path.get())
            file = common.file_from_list_of_images(file_list,
                                                   current_file,
                                                   "last")
            if file is not None:
                try:
                    file_select_L.configure(text=file)
                    file_in_path.set(os.path.normpath(os.path.join(cwd, file)))
                    preview_orig()
                except:
                    print("Error in open_file_last")


def open_file_next():
    """ Open next file """
    if file_in_path.get():
        if os.path.isfile(file_in_path.get()):
            cwd = os.path.dirname(file_in_path.get())
            file_list = common.list_of_images(cwd)
            current_file = os.path.basename(file_in_path.get())
            file = common.file_from_list_of_images(file_list,
                                                   current_file,
                                                   "next")
            if file is not None:
                try:
                    file_select_L.configure(text=file)
                    file_in_path.set(os.path.normpath(os.path.join(cwd, file)))
                    preview_orig()
                except:
                    print("Error in open_file_next")


def open_file_first():
    """ Open first file """
    if file_in_path.get():
        if os.path.isfile(file_in_path.get()):
            cwd = os.path.dirname(file_in_path.get())
            file_list = common.list_of_images(cwd)
            current_file = os.path.basename(file_in_path.get())
            file = common.file_from_list_of_images(file_list,
                                                   current_file,
                                                   "first")
            if file is not None:
                try:
                    file_select_L.configure(text=file)
                    file_in_path.set(os.path.normpath(os.path.join(cwd, file)))
                    preview_orig()
                except:
                    print("Error in open_file_first")


def open_file_prev():
    """ Open previous file """
    if file_in_path.get():
        if os.path.isfile(file_in_path.get()):
            cwd = os.path.dirname(file_in_path.get())
            file_list = common.list_of_images(cwd)
            current_file = os.path.basename(file_in_path.get())
            file = common.file_from_list_of_images(file_list,
                                                   current_file,
                                                   "previous")
            if file is not None:
                try:
                    file_select_L.configure(text=file)
                    file_in_path.set(os.path.normpath(os.path.join(cwd, file)))
                    preview_orig()
                except:
                    print("Error in open_file_first")

                file_select_L.configure(text=file)

                directory = os.path.dirname(file_in_path.get())
                file_in_path.set(os.path.join(directory, file))
                preview_orig()


def color_choose_border():
    """ Border color selection """
    color = askcolor(img_border_color.get())
    if color[1] is None:
        img_border_color.set("#000000")
    else:
        img_border_color.set(color[1])
        l_border.configure(bg=img_border_color.get())


def color_choose_box_active():
    """ Activate background color """
    if img_text_box.get() == 0:
        l_text_font_selected.configure(bg="#000000")
    else:
        l_text_font_selected.configure(bg=img_text_box_color.get())


def color_choose_box():
    """ Background color selection """
    if img_text_box.get() != 0:
        color = askcolor(img_text_color.get(), root)
        if color[1] is None:
            img_text_box_color.set("#FFFFFF")
        else:
            img_text_box_color.set(color[1])
            l_text_font_selected.configure(bg=img_text_box_color.get())


def color_choose():
    """ Color selection """
    color = askcolor(img_text_color.get(), root)
    if color[1] is None:
        img_text_color.set("#FFFFFF")
    else:
        img_text_color.set(color[1])
    l_text_font_selected.configure(fg=img_text_color.get())


def ini_read_wraper():
    """ Read config INI file """

    ini_entries = ini_read.ini_read(FILE_INI)
    file_in_path.set(ini_entries['file_in_path'])
    file_dir_selector.set(ini_entries['file_dir_selector'])
    work_dir.set(ini_entries['work_dir'])
    img_histograms_on.set(ini_entries['img_histograms_on'])

    ini_entries = ini_read.ini_read_resize(FILE_INI)
    img_resize_on.set(ini_entries['img_resize_on'])
    img_resize.set(ini_entries['img_resize'])
    e1_resize.delete(0, "end")
    e1_resize.insert(0, ini_entries['resize_size_pixel'])
    e2_resize.delete(0, "end")
    e2_resize.insert(0, ini_entries['resize_size_percent'])

    ini_entries = ini_read.ini_read_text(FILE_INI)
    img_text_on.set(ini_entries['img_text_on'])
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
    img_rotate_on.set(ini_entries['img_rotate_on'])
    img_rotate.set(ini_entries['img_rotate'])

    ini_entries = ini_read.ini_read_crop(FILE_INI)
    img_crop_on.set(ini_entries['img_crop_on'])
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
    img_border_on.set(ini_entries['img_border_on'])
    img_border_color.set(ini_entries['img_border_color'])
    l_border.configure(bg=ini_entries['img_border_color'])
    e_border.delete(0, "end")
    e_border.insert(0, ini_entries['img_border_size'])

    ini_entries = ini_read.ini_read_color(FILE_INI)
    img_bw_on.set(ini_entries['color_on'])
    img_bw.set(ini_entries['black_white'])
    e_bw_sepia.delete(0, "end")
    e_bw_sepia.insert(0, ini_entries['sepia'])

    ini_entries = ini_read.ini_read_normalize(FILE_INI)
    img_normalize_on.set(ini_entries['normalize_on'])
    img_normalize.set(ini_entries['normalize'])

    ini_entries = ini_read.ini_read_contrast(FILE_INI)
    img_contrast_on.set(ini_entries['contrast_on'])
    img_contrast.set(ini_entries['contrast'])
    cb_contrast.current(str(img_contrast.get()))
    e1_contrast.delete(0, "end")
    e1_contrast.insert(0, ini_entries['contrast_stretch_1'])
    e2_contrast.delete(0, "end")
    e2_contrast.insert(0, ini_entries['contrast_stretch_2'])

    ini_entries = ini_read.ini_read_custom(FILE_INI)
    img_custom_on.set(ini_entries['custom_on'])

    ini_entries = ini_read.ini_read_logo(FILE_INI)
    img_logo_on.set(ini_entries['img_logo_on'])
    file_logo_path.set(ini_entries['logo_logo'])
    img_logo_gravity.set(ini_entries['img_logo_gravity'])
    e_logo_width.delete(0, "end")
    e_logo_width.insert(0, ini_entries['logo_width'])
    e_logo_height.delete(0, "end")
    e_logo_height.insert(0, ini_entries['logo_height'])
    e_logo_dx.delete(0, "end")
    e_logo_dx.insert(0, ini_entries['logo_dx'])
    e_logo_dy.delete(0, "end")
    e_logo_dy.insert(0, ini_entries['logo_dy'])


def ini_save():
    """ Write variables into config file INI """

    # content preparing
    config = configparser.ConfigParser()
    config.add_section('Konfiguracja')
    config.set('Konfiguracja', 'path', file_in_path.get())
    config.set('Konfiguracja', 'work_dir', work_dir.get())
    config.set('Konfiguracja', 'file_dir', str(file_dir_selector.get()))
    config.set('Konfiguracja', 'histograms', str(img_histograms_on.get()))
    config.add_section('Resize')
    config.set('Resize', 'on', str(img_resize_on.get()))
    config.set('Resize', 'resize', str(img_resize.get()))
    config.set('Resize', 'size_pixel', e1_resize.get())
    config.set('Resize', 'size_percent', e2_resize.get())
    config.add_section('Text')
    config.set('Text', 'on', str(img_text_on.get()))
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
    config.set('Rotate', 'on', str(img_rotate_on.get()))
    config.set('Rotate', 'rotate', str(img_rotate.get()))
    config.add_section('Crop')
    config.set('Crop', 'on', str(img_crop_on.get()))
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
    config.set('Border', 'on', str(img_border_on.get()))
    config.set('Border', 'color', img_border_color.get())
    config.set('Border', 'size', e_border.get())
    config.add_section('Color')
    config.set('Color', 'on', str(img_bw_on.get()))
    config.set('Color', 'black-white', str(img_bw.get()))
    config.set('Color', 'sepia', e_bw_sepia.get())
    config.add_section('Normalize')
    config.set('Normalize', 'on', str(img_normalize_on.get()))
    config.set('Normalize', 'normalize', str(img_normalize.get()))
    config.add_section('Contrast')
    config.set('Contrast', 'on', str(img_contrast_on.get()))
    config.set('Contrast', 'contrast', str(img_contrast.get()))
    config.set('Contrast', 'contrast_stretch_1', e1_contrast.get())
    config.set('Contrast', 'contrast_stretch_2', e2_contrast.get())
    config.add_section('Logo')
    config.set('Logo', 'on', str(img_logo_on.get()))
    config.set('Logo', 'logo', file_logo_path.get())
    config.set('Logo', 'gravity', img_logo_gravity.get())
    config.set('Logo', 'width', e_logo_width.get())
    config.set('Logo', 'height', e_logo_height.get())
    config.set('Logo', 'dx', e_logo_dx.get())
    config.set('Logo', 'dy', e_logo_dy.get())
    config.add_section('Custom')
    config.set('Custom', 'on', str(img_custom_on.get()))

    # save to a file
    try:
        with open(FILE_INI, 'w', encoding='utf-8', buffering=1) as configfile:
            config.write(configfile)
    except:
        print("! Error in ini_save: cannot save config file: " + FILE_INI)


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
        print("! Error in help_info: error during loading license file")
        message = "Copyright 2019 Tomasz Łuczak under MIT license"

    messagebox.showinfo(title=_("License"), message=message)


def close_window():
    """ close program """
    root.quit()
    root.destroy()
    sys.exit()


def win_deleted():
    """ close program window """
    print("closed")
    close_window()


def mouse_crop_NW(event):
    """ Left-Upper corner """
    x_preview = event.x
    y_preview = event.y
    # print("NW preview:", x_preview, y_preview)

    xy_max = common.mouse_crop_calculation(file_in_path.get(), PREVIEW_ORIG)
    width = int(x_preview*xy_max['x_orig']/xy_max['x_max'])
    height = int(y_preview*xy_max['y_orig']/xy_max['y_max'])
    e1_crop_1.delete(0, "end")
    e1_crop_1.insert(0, width)
    e2_crop_1.delete(0, "end")
    e2_crop_1.insert(0, height)


def mouse_crop_SE(event):
    """ Right-Lower corner """
    x_preview = event.x
    y_preview = event.y
    # print("SE preview:", x_preview, y_preview)
    xy_max = common.mouse_crop_calculation(file_in_path.get(), PREVIEW_ORIG)
    width = int(x_preview*xy_max['x_orig']/xy_max['x_max'])
    height = int(y_preview*xy_max['y_orig']/xy_max['y_max'])
    e3_crop_1.delete(0, "end")
    e3_crop_1.insert(0, width)
    e4_crop_1.delete(0, "end")
    e4_crop_1.insert(0, height)


def preview_orig():
    """
    generation preview of originalpicture
    and add crop rectangle
    """
    if img_crop_on.get() == 1:
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
    else:
        do_nothing = 1

    if do_nothing != 1:
        xy_max = common.mouse_crop_calculation(file_in_path.get(), PREVIEW_ORIG)
        ratio_X = xy_max['x_max'] / xy_max['x_orig']
        ratio_Y = xy_max['y_max'] / xy_max['y_orig']
        x0 = int(x0 * ratio_X)
        y0 = int(y0 * ratio_Y)
        x1 = int(x1 * ratio_X)
        y1 = int(y1 * ratio_Y)

        x0y0x1y1 = str(x0) + "," + str(y0) + " " + str(x1) + "," + str(y1)
        command = " -fill none  -draw \"stroke '#FFFF00' rectangle " \
            + x0y0x1y1 + "\" "
    else:
        command = " "

    preview_picture = preview.preview_convert(file_in_path.get(),
                                              TEMP_DIR,
                                              command,
                                              PREVIEW_ORIG)
    try:
        pi_preview_orig.configure(file=common.spacja(preview_picture['filename']))
    except:
        print("! Error in preview_orig: Cannot load preview")

    try:
        l_preview_orig.configure(text=preview_picture['width'] + "x"\
                                 + preview_picture['height'])
    except:
        print("! Error in preview_orig: Cannot load image size")

    if img_histograms_on.get() == 1:
        try:
            pi_histogram_orig.configure(file=preview.preview_histogram(file_in_path.get(),
                                                                       TEMP_DIR))
        except:
            print("! Error in preview_orig: : Cannot load histogram preview")


def preview_logo():
    """ generating logo preview """

    l_logo_filename.configure(text=os.path.basename(file_logo_path.get()))

    preview_picture = preview.preview_convert(file_logo_path.get(),
                                              TEMP_DIR,
                                              " ",
                                              PREVIEW_LOGO)
    try:
        pi_logo_preview.configure(file=preview_picture['filename'])
        # l_logo_preview.configure(text=preview['width'] + "x" + preview['height'])
    except:
        print("! Error in preview_logo: Cannot load preview")


def tools_set():
    """ wybór narzędzi do wyświetlenia """

    if img_custom_on.get() == 1:
        frame_custom.grid()
#        img_resize_on.set(0)
#        img_crop_on.set(0)
#        img_text_on.set(0)
#        img_rotate_on.set(0)
#        img_border_on.set(0)
#        img_bw_on.set(0)
#        img_contrast_on.set(0)
#        img_normalize_on.set(0)
#        img_logo_on.set(0)
    else:
        frame_custom.grid_remove()

    if img_histograms_on.get() == 0:
        frame_histogram_orig.grid_remove()
        frame_histogram_new.grid_remove()
    else:
        frame_histogram_orig.grid()
        frame_histogram_new.grid()

    if img_resize_on.get() == 0:
        frame_resize.grid_remove()
    else:
        frame_resize.grid()

    if img_crop_on.get() == 0:
        frame_crop.grid_remove()
    else:
        frame_crop.grid()

    if img_text_on.get() == 0:
        frame_text.grid_remove()
    else:
        frame_text.grid()

    if img_rotate_on.get() == 0:
        frame_rotate.grid_remove()
    else:
        frame_rotate.grid()

    if img_border_on.get() == 0:
        frame_border.grid_remove()
    else:
        frame_border.grid()

    if img_bw_on.get() == 0:
        frame_bw.grid_remove()
    else:
        frame_bw.grid()

    if img_contrast_on.get() == 0:
        frame_contrast.grid_remove()
    else:
        frame_contrast.grid()

    if img_normalize_on.get() == 0:
        frame_normalize.grid_remove()
    else:
        frame_normalize.grid()

    if img_logo_on.get() == 0:
        frame_logo.grid_remove()
    else:
        frame_logo.grid()

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
file_in_path = StringVar()  # fullpath original picture
file_logo_path = StringVar()  # fullpath logo file
img_logo_gravity = StringVar()
img_resize = IntVar()
img_text_gravity = StringVar()
img_rotate = IntVar()
img_text_font = StringVar()
img_text_font_list = StringVar()
img_text_color = StringVar()
img_text_box = IntVar()
img_text_box_color = StringVar()
img_crop = IntVar()
img_crop_gravity = StringVar()
img_border_color = StringVar()
img_normalize = IntVar()
img_bw = IntVar()
img_contrast = IntVar()
img_contrast_selected = StringVar()
img_histograms_on = IntVar()
img_logo_on = IntVar()
img_resize_on = IntVar()
img_text_on = IntVar()
img_rotate_on = IntVar()
img_crop_on = IntVar()
img_border_on = IntVar()
img_normalize_on = IntVar()
img_bw_on = IntVar()
img_contrast_on = IntVar()
img_custom_on = IntVar()
progress_var = IntVar()  # progressbar
progress_files = StringVar()
imagick_commands = ("animate",
                    "compare",
                    "composite",
                    "conjure",
                    "convert",
                    "identify",
                    "import",
                    "mogrify",
                    "montage",
                    "stream")
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

cb_histograms = ttk.Checkbutton(frame_zero_set,
                                text=_("Histograms"),
                                variable=img_histograms_on,
                                offvalue="0", onvalue="1")
cb_resize = ttk.Checkbutton(frame_zero_set,
                            text=_("Scaling/Resize"),
                            variable=img_resize_on,
                            offvalue="0",
                            onvalue="1")
cb_crop = ttk.Checkbutton(frame_zero_set,
                          text=_("Crop"),
                          variable=img_crop_on,
                          offvalue="0", onvalue="1")
cb_text = ttk.Checkbutton(frame_zero_set,
                          text=_("Text"),
                          variable=img_text_on,
                          onvalue="1",
                          offvalue="0")
cb_rotate = ttk.Checkbutton(frame_zero_set,
                            text=_("Rotate"),
                            variable=img_rotate_on,
                            offvalue="0",
                            onvalue="1")
cb_border = ttk.Checkbutton(frame_zero_set,
                            text=_("Frame"),
                            variable=img_border_on,
                            offvalue="0",
                            onvalue="1")
cb_bw = ttk.Checkbutton(frame_zero_set,
                        text=_("Black&white"),
                        variable=img_bw_on,
                        offvalue="0")
cb_normalize = ttk.Checkbutton(frame_zero_set,
                               text=_("Colors normalize"),
                               variable=img_normalize_on,
                               offvalue="0",
                               onvalue="1")
cb_contrast = ttk.Checkbutton(frame_zero_set,
                              text=_("Contrast"),
                              variable=img_contrast_on,
                              offvalue="0",
                              onvalue="1")
cb_logo = ttk.Checkbutton(frame_zero_set,
                          text=_("Logo"),
                          variable=img_logo_on,
                          offvalue="0",
                          onvalue="1")
cb_custom = ttk.Checkbutton(frame_zero_set,
                            text=_("Custom"),
                            variable=img_custom_on,
                            offvalue="0",
                            onvalue="1")
b_last_set = ttk.Button(frame_zero_set, text=_("Apply"), command=tools_set)

cb_histograms.pack(padx=5, pady=5, anchor=W)
cb_resize.pack(padx=5, pady=5, anchor=W)
cb_crop.pack(padx=5, pady=5, anchor=W)
cb_text.pack(padx=5, pady=5, anchor=W)
cb_rotate.pack(padx=5, pady=5, anchor=W)
cb_border.pack(padx=5, pady=5, anchor=W)
cb_bw.pack(padx=5, pady=5, anchor=W)
cb_contrast.pack(padx=5, pady=5, anchor=W)
cb_normalize.pack(padx=5, pady=5, anchor=W)
cb_logo.pack(padx=5, pady=5, anchor=W)
cb_custom.pack(padx=5, pady=10, anchor=W)

b_last_set.pack(padx=5, pady=5)
###########################
# Przyciski
###########################
frame_zero_cmd = ttk.Labelframe(frame_zero_col,
                                text=_("Settings"),
                                style="Blue.TLabelframe")
frame_zero_cmd.grid(row=2, column=1, padx=5, pady=5, sticky=(W, E))

b_last_save = ttk.Button(frame_zero_cmd,
                         text=_("Save"),
                         command=ini_save)
b_last_read = ttk.Button(frame_zero_cmd,
                         text=_("Load"),
                         command=ini_read_wraper)

b_last_save.grid(row=1, column=1, pady=5)
b_last_read.grid(row=1, column=2, padx=5, pady=5)

###########################
# Logo
###########################
frame_logo = ttk.Labelframe(frame_zero_col,
                            text=_("Logo"),
                            style="Blue.TLabelframe")
frame_logo.grid(row=3, column=1, sticky=(N, W, E, S), padx=5, pady=5)

b_logo_select = ttk.Button(frame_logo,
                           text=_("File selection"),
                           command=open_file_logo)

b_logo_run = ttk.Button(frame_logo,
                        text=_("Execute"),
                        command=convert_logo_button,
                        style="Blue.TButton")
l_logo_filename = ttk.Label(frame_logo, width=25)

b_logo_select.grid(row=1, column=1, pady=5)
b_logo_run.grid(row=1, column=2, pady=5)
l_logo_filename.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=W)

###
frame_logo_xy = ttk.Frame(frame_logo)
l_logo_XxY = ttk.Label(frame_logo_xy, text=_("Width\nHeight"))
l_logo_dxdy = ttk.Label(frame_logo_xy, text=_("Offset\n(dx,dy)"))
e_logo_width = ttk.Entry(frame_logo_xy, width=3)
e_logo_height = ttk.Entry(frame_logo_xy, width=3)
e_logo_dx = ttk.Entry(frame_logo_xy, width=3)
e_logo_dy = ttk.Entry(frame_logo_xy, width=3)

frame_logo_xy.grid(row=3, column=1, columnspan=2)
l_logo_XxY.grid(row=2, column=1, sticky=W, padx=5)
e_logo_width.grid(row=2, column=2, sticky=W, padx=5)
e_logo_height.grid(row=2, column=3, sticky=W, padx=5)
l_logo_dxdy.grid(row=3, column=1, sticky=W, padx=5)
e_logo_dx.grid(row=3, column=2, sticky=W, padx=5)
e_logo_dy.grid(row=3, column=3, sticky=W, padx=5)

###
frame_logo_gravity = ttk.Frame(frame_logo)
rb_logo_NW = ttk.Radiobutton(frame_logo_gravity, text="NW",
                             variable=img_logo_gravity, value="NW")
rb_logo_N = ttk.Radiobutton(frame_logo_gravity, text="N",
                            variable=img_logo_gravity, value="N")
rb_logo_NE = ttk.Radiobutton(frame_logo_gravity, text="NE",
                             variable=img_logo_gravity, value="NE")
rb_logo_W = ttk.Radiobutton(frame_logo_gravity, text="W",
                            variable=img_logo_gravity, value="W")
rb_logo_C = ttk.Radiobutton(frame_logo_gravity, text=_("Center"),
                            variable=img_logo_gravity, value="C")
rb_logo_E = ttk.Radiobutton(frame_logo_gravity, text="E",
                            variable=img_logo_gravity, value="E")
rb_logo_SW = ttk.Radiobutton(frame_logo_gravity, text="SW",
                             variable=img_logo_gravity, value="SW")
rb_logo_S = ttk.Radiobutton(frame_logo_gravity, text="S",
                            variable=img_logo_gravity, value="S")
rb_logo_SE = ttk.Radiobutton(frame_logo_gravity, text="SE",
                             variable=img_logo_gravity, value="SE")
frame_logo_gravity.grid(row=4, column=1, columnspan=2)
rb_logo_NW.grid(row=1, column=1, sticky=W, pady=5)
rb_logo_N.grid(row=1, column=2, pady=5)
rb_logo_NE.grid(row=1, column=3, sticky=W, pady=5)
rb_logo_W.grid(row=2, column=1, sticky=W, pady=5)
rb_logo_C.grid(row=2, column=2, pady=5)
rb_logo_E.grid(row=2, column=3, sticky=W, pady=5)
rb_logo_SW.grid(row=3, column=1, sticky=W, pady=5)
rb_logo_S.grid(row=3, column=2, pady=5)
rb_logo_SE.grid(row=3, column=3, sticky=W, pady=5)

###
pi_logo_preview = PhotoImage()
l_logo_preview_pi = ttk.Label(frame_logo, image=pi_logo_preview)
l_logo_preview_pi.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

#####################################################################
# First column
#####################################################################
frame_first_col = ttk.Frame(main)
frame_first_col.grid(row=1, column=2, rowspan=2, sticky=(N, W, E, S))

###########################
# Resize
###########################
frame_resize = ttk.Labelframe(frame_first_col,
                              text=_("Scale/Resize"),
                              style="Blue.TLabelframe")
frame_resize.grid(column=1, row=2, columnspan=2,
                  sticky=(N, W, E, S),
                  padx=5, pady=5)
###
rb_1_resize = ttk.Radiobutton(frame_resize,
                              text=_("Pixels"),
                              variable=img_resize,
                              value="1")
e1_resize = ttk.Entry(frame_resize, width=7)
rb_2_resize = ttk.Radiobutton(frame_resize,
                              text=_("Percent"),
                              variable=img_resize,
                              value="2")
e2_resize = ttk.Entry(frame_resize, width=7)
rb_3_resize = ttk.Radiobutton(frame_resize,
                              text="FullHD (1920x1080)",
                              variable=img_resize,
                              value="3")
rb_4_resize = ttk.Radiobutton(frame_resize,
                              text="2K (2048×1556)",
                              variable=img_resize,
                              value="4")
rb_5_resize = ttk.Radiobutton(frame_resize,
                              text="4K (4096×3112)",
                              variable=img_resize,
                              value="5")
b_resize = ttk.Button(frame_resize, text=_("Resize"),
                      style="Blue.TButton",
                      command=convert_resize_button)

rb_3_resize.grid(row=1, column=1, columnspan=2, sticky=W, padx=5, pady=5)
rb_4_resize.grid(row=1, column=3, columnspan=2, sticky=W, padx=5, pady=5)
rb_5_resize.grid(row=1, column=5, sticky=W, padx=5, pady=5)
rb_1_resize.grid(row=2, column=1, sticky=W, padx=5, pady=5)
e1_resize.grid(row=2, column=2, sticky=W, padx=5, pady=5)
rb_2_resize.grid(row=2, column=3, sticky=W, padx=5, pady=5)
e2_resize.grid(row=2, column=4, sticky=W, padx=5, pady=5)
b_resize.grid(row=2, column=5, sticky=(E), padx=5, pady=5)

############################
# crop
############################
frame_crop = ttk.Labelframe(frame_first_col,
                            text=_("Crop"),
                            style="Blue.TLabelframe")
frame_crop.grid(row=3, column=1, columnspan=2,
                sticky=(N, W, E, S),
                padx=5, pady=5)
###
rb1_crop = ttk.Radiobutton(frame_crop,
                           variable=img_crop,
                           value="1",
                           text=_("Coordinates (x1, y1) and (x2, y2)"))
f_clickL_crop = ttk.Labelframe(frame_crop, text=_("Left Upper corner"))
l_clickL_crop = ttk.Label(f_clickL_crop, text=_("Click left"))
e1_crop_1 = ttk.Entry(f_clickL_crop, width=4)
e2_crop_1 = ttk.Entry(f_clickL_crop, width=4)
f_clickR_crop = ttk.Labelframe(frame_crop, text=_("Right lower corner"))
l_clickR_crop = ttk.Label(f_clickR_crop, text=_("Click right"))
e3_crop_1 = ttk.Entry(f_clickR_crop, width=4)
e4_crop_1 = ttk.Entry(f_clickR_crop, width=4)

rb2_crop = ttk.Radiobutton(frame_crop,
                           variable=img_crop,
                           value="2",
                           text=_("Origin (x1,y1) and dimensions (X, Y)"))
e1_crop_2 = ttk.Entry(frame_crop, width=4)
e2_crop_2 = ttk.Entry(frame_crop, width=4)
e3_crop_2 = ttk.Entry(frame_crop, width=4)
e4_crop_2 = ttk.Entry(frame_crop, width=4)

rb3_crop = ttk.Radiobutton(frame_crop,
                           variable=img_crop,
                           value="3",
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
rbC_crop_3 = ttk.Radiobutton(frame_crop_gravity, text=_("Center"),
                             variable=img_crop_gravity, value="C")
rbE_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="E",
                             variable=img_crop_gravity, value="E")
rbSW_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="SW",
                              variable=img_crop_gravity, value="SW")
rbS_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="S",
                             variable=img_crop_gravity, value="S")
rbSE_crop_3 = ttk.Radiobutton(frame_crop_gravity, text="SE",
                              variable=img_crop_gravity, value="SE")

b_crop_read = ttk.Button(frame_crop,
                         text=_("From image"),
                         command=crop_read)
b_crop = ttk.Button(frame_crop,
                    text=_("Crop"),
                    style="Blue.TButton",
                    command=convert_crop_button)

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
frame_crop_gravity.grid(row=5, column=4, columnspan=3)
rbNW_crop_3.grid(row=1, column=1, sticky=W, pady=5)
rbN_crop_3.grid(row=1, column=2, pady=5)
rbNE_crop_3.grid(row=1, column=3, sticky=W, pady=5)
rbW_crop_3.grid(row=2, column=1, sticky=W, pady=5)
rbC_crop_3.grid(row=2, column=2, sticky=W, pady=5)
rbE_crop_3.grid(row=2, column=3, sticky=W, pady=5)
rbSW_crop_3.grid(row=3, column=1, sticky=W, pady=5)
rbS_crop_3.grid(row=3, column=2, pady=5)
rbSE_crop_3.grid(row=3, column=3, sticky=W, pady=5)
b_crop_read.grid(row=5, column=2, columnspan=2, sticky=W, padx=5, pady=5)
b_crop.grid(row=5, column=1, sticky=W, padx=5, pady=5)

###########################
# Tekst
###########################
frame_text = ttk.Labelframe(frame_first_col,
                            text=_("Add text"),
                            style="Blue.TLabelframe")
frame_text.grid(row=4, column=1, columnspan=2,
                sticky=(N, W, E, S),
                padx=5, pady=5)
###
frame_text_text = ttk.Frame(frame_text)

e_text = ttk.Entry(frame_text_text, width=60)
frame_text_text.grid(row=1, column=1, columnspan=5, sticky=(W, E))
e_text.grid(row=1, column=2, sticky=W, padx=5)
# cb_text_on.grid(row=1, column=3, sticky=W, padx=5)
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
rbC = ttk.Radiobutton(frame_text_gravity, text=_("Center"),
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
cb_text_font.configure(state='readonly')
e_text_size = ttk.Entry(frame_text_font, width=3)
b_text_color = ttk.Button(frame_text,
                          text=_("Font color"),
                          command=color_choose)
cb_text_box = ttk.Checkbutton(frame_text_font,
                              text=_("Background"),
                              variable=img_text_box,
                              onvalue="1",
                              offvalue="0",
                              command=color_choose_box_active)
b_text_box_color = ttk.Button(frame_text,
                              text=_("Background color"),
                              command=color_choose_box)
l_text_windows = ttk.Label(frame_text, width=40)
b_text = ttk.Button(frame_text,
                    text=_("Put text"),
                    style="Blue.TButton",
                    command=convert_text_button)
l_text_font_selected = Label(frame_text, width=20, textvariable=img_text_font)

l_text_font_selected.grid(row=3, column=1, sticky=(W, E), padx=5)
b_text_color.grid(row=3, column=3, sticky=(W, E), padx=5, pady=5)
b_text_box_color.grid(row=3, column=4, sticky=(W, E), padx=5, pady=5)
frame_text_font.grid(row=4, column=1, columnspan=4, sticky=(W, E))
cb_text_font.grid(row=1, column=1, sticky=(W, E), padx=5)
e_text_size.grid(row=1, column=2, sticky=W, padx=5)
cb_text_box.grid(row=1, column=3, sticky=W, padx=5)
b_text.grid(row=4, column=4, sticky=(W, E), padx=5, pady=5)
l_text_windows.grid(row=5, column=1, columnspan=4, sticky=(W, E))

###########################
# Rotate
###########################
frame_rotate = ttk.Labelframe(frame_first_col,
                              text=_("Rotate"),
                              style="Blue.TLabelframe")
frame_rotate.grid(row=5, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
rb_rotate_0 = ttk.Radiobutton(frame_rotate,
                              text="0",
                              variable=img_rotate,
                              value="0")
rb_rotate_90 = ttk.Radiobutton(frame_rotate,
                               text="90",
                               variable=img_rotate,
                               value="90")
rb_rotate_180 = ttk.Radiobutton(frame_rotate,
                                text="180",
                                variable=img_rotate,
                                value="180")
rb_rotate_270 = ttk.Radiobutton(frame_rotate,
                                text="270",
                                variable=img_rotate,
                                value="270")
b_rotate = ttk.Button(frame_rotate, text=_("Rotate"),
                      style="Blue.TButton",
                      command=convert_rotate_button)

rb_rotate_0.grid(row=1, column=1, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_90.grid(row=1, column=2, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_180.grid(row=1, column=3, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_270.grid(row=1, column=4, sticky=(N, W, E, S), padx=5, pady=5)
b_rotate.grid(row=1, column=5, padx=5, pady=5)

############################
# Black-white
############################
frame_bw = ttk.LabelFrame(frame_first_col,
                          text=_("Black-white"),
                          style="Blue.TLabelframe")
frame_bw.grid(row=5, column=2, rowspan=2, sticky=(N, W, E, S), padx=5, pady=5)
###
rb1_bw = ttk.Radiobutton(frame_bw,
                         text=_("Black-white"),
                         variable=img_bw,
                         value="1")
rb2_bw = ttk.Radiobutton(frame_bw,
                         text=_("Sepia"),
                         variable=img_bw,
                         value="2")
e_bw_sepia = ttk.Entry(frame_bw, width=3)
l_bw_sepia = ttk.Label(frame_bw, text="%")
b_bw = ttk.Button(frame_bw, text=_("Execute"),
                  style="Blue.TButton",
                  command=convert_bw_button)


rb2_bw.grid(row=1, column=1, padx=5, pady=5, sticky=W)
e_bw_sepia.grid(row=1, column=2, padx=5, pady=5, sticky=E)
l_bw_sepia.grid(row=1, column=3, padx=5, pady=5, sticky=W)
rb1_bw.grid(row=2, column=1, padx=5, pady=5, sticky=W)
b_bw.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=E)

###########################
# Border
###########################
frame_border = ttk.Labelframe(frame_first_col,
                              text=_("Frame"),
                              style="Blue.TLabelframe")
frame_border.grid(row=6, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
l_border = Label(frame_border, text=_("Pixels"))
e_border = ttk.Entry(frame_border, width=3)
b1_border = ttk.Button(frame_border,
                       text=_("Color"),
                       command=color_choose_border)
b_border = ttk.Button(frame_border,
                      text=_("Add frame"),
                      style="Blue.TButton",
                      command=convert_border_button)

l_border.grid(row=1, column=1, padx=5, pady=5)
e_border.grid(row=1, column=2, padx=5, pady=5)
b1_border.grid(row=1, column=3, padx=5, pady=5)
b_border.grid(row=1, column=4, padx=5, pady=5, sticky=E)


########################
# Contrast
#########################
frame_contrast = ttk.Labelframe(frame_first_col,
                                text=_("Contrast"),
                                style="Blue.TLabelframe")
frame_contrast.grid(row=7, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
b_contrast = ttk.Button(frame_contrast,
                        text=_("Contrast"),
                        style="Blue.TButton",
                        command=convert_contrast_button)
rb1_contrast = ttk.Radiobutton(frame_contrast,
                               text=_("Contrast"),
                               variable=img_contrast,
                               value="1")
cb_contrast = ttk.Combobox(frame_contrast,
                           width=2,
                           values=("+3", "+2", "+1", "0", "-1", "-2", "-3"))
rb2_contrast = ttk.Radiobutton(frame_contrast,
                               text=_("Stretch"),
                               variable=img_contrast,
                               value="2")
e1_contrast = ttk.Entry(frame_contrast, width=4)
e2_contrast = ttk.Entry(frame_contrast, width=4)
l1_contrast = ttk.Label(frame_contrast, text=_("Black"))
l2_contrast = ttk.Label(frame_contrast, text=_("White"))


rb2_contrast.grid(row=2, column=1, padx=5, pady=5, sticky=W)
l1_contrast.grid(row=2, column=2, padx=5, pady=5, sticky=E)
e1_contrast.grid(row=2, column=3, padx=5, pady=5, sticky=E)
l2_contrast.grid(row=2, column=4, padx=5, pady=5, sticky=W)
e2_contrast.grid(row=2, column=5, padx=5, pady=5, sticky=W)
rb1_contrast.grid(row=3, column=1, padx=5, pady=5, sticky=W)
cb_contrast.grid(row=3, column=2, padx=5, pady=5, sticky=W)
b_contrast.grid(row=3, column=3, padx=5, pady=5, columnspan=3, sticky=E)

############################
# Normalize
############################
frame_normalize = ttk.LabelFrame(frame_first_col,
                                 text=_("Color normalize"),
                                 style="Blue.TLabelframe")
frame_normalize.grid(row=7, column=2, sticky=(N, W, E, S), padx=5, pady=5)
###
rb1_normalize = ttk.Radiobutton(frame_normalize,
                                text=_("Normalize"),
                                variable=img_normalize,
                                value="1")
rb2_normalize = ttk.Radiobutton(frame_normalize,
                                text=_("AutoLevel"),
                                variable=img_normalize,
                                value="2")
b_normalize = ttk.Button(frame_normalize,
                         text=_("Normalize"),
                         style="Blue.TButton",
                         command=convert_normalize_button)

rb1_normalize.grid(row=1, column=1, padx=5, pady=5, sticky=W)
rb2_normalize.grid(row=1, column=2, padx=5, pady=5, sticky=W)
b_normalize.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=E)


############################
# Custom command
############################
frame_custom = ttk.LabelFrame(frame_first_col,
                              text=_("Custom command"),
                              style="Blue.TLabelframe")
frame_custom.grid(row=10, column=1, columnspan=2,
                  sticky=(N, W, E, S),
                  padx=5, pady=5)
###
l_custom_command = ttk.Label(frame_custom, text=_("Command"))
cb_custom_command = ttk.Combobox(frame_custom,
                                 width=9,
                                 values=imagick_commands)
cb_custom_command.current(7)

b_custom = ttk.Button(frame_custom,
                      text=_("Execute"),
                      style="Blue.TButton",
                      command=convert_custom_button)

t_custom = ScrolledText(frame_custom,
                        state='normal',
                        height=5, width=70,
                        wrap='word', undo=True)

# configuring a tag with a certain style (font color)
# t_custom.tag_configure("blue", foreground="blue")

# apply the tag
#t_custom.highlight_pattern("-resize", "blue")
#t_custom.highlight_pattern("-crop", "blue")
#t_custom.highlight_pattern("-gravity", "blue")
#t_custom.highlight_pattern("-draw", "blue")
#t_custom.highlight_pattern("-border", "blue")

l_custom_command.grid(row=1, column=1, padx=5, pady=5, sticky=W)
cb_custom_command.grid(row=1, column=2, padx=5, pady=5, sticky=W)
b_custom.grid(row=1, column=3, padx=5, pady=5, sticky=W)
t_custom.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=W)

########################################################################
# Second column
########################################################################
frame_second_col = ttk.Frame(main)
frame_second_col.grid(row=1, column=3, sticky=(N, W, E, S))

###########################
# Picture selection
###########################
frame_input = ttk.Labelframe(frame_second_col, text=_("Image"),
                             style="Blue.TLabelframe")
frame_input.grid(row=1, column=1, sticky=(N, W, E, S), padx=5, pady=5)

b_file_select = ttk.Button(frame_input, text=_("File selection"),
                           command=open_file, style="Blue.TButton")

file_select_L = ttk.Label(frame_input, width=24)


b_file_select_first = ttk.Button(frame_input, text=_("First"),
                                 command=open_file_first)
b_file_select_prev = ttk.Button(frame_input, text=_("Previous"),
                                command=open_file_prev)
b_file_select_next = ttk.Button(frame_input, text=_("Next"),
                                command=open_file_next)
b_file_select_last = ttk.Button(frame_input, text=_("Last"),
                                command=open_file_last)

b_file_select.grid(column=1, row=1, padx=5, pady=5, sticky=W)
file_select_L.grid(column=2, row=1, padx=5, pady=5, sticky=W, columnspan=3)
#
b_file_select_first.grid(column=1, row=2, padx=5, pady=5, sticky=W)
b_file_select_prev.grid(column=2, row=2, padx=5, pady=5, sticky=W)
b_file_select_next.grid(column=3, row=2, padx=5, pady=5, sticky=W)
b_file_select_last.grid(column=4, row=2, padx=5, pady=5, sticky=W)

############################
# Original preview
############################
frame_preview_orig = ttk.Labelframe(frame_second_col,
                                    text=_("Original"),
                                    style="Blue.TLabelframe")
frame_preview_orig.grid(row=2, column=1, columnspan=2,
                        sticky=(N, W, E, S),
                        padx=5, pady=5)
###
b_preview_orig = ttk.Button(frame_preview_orig,
                            text=_("Preview"),
                            command=preview_orig_button)
l_preview_orig = ttk.Label(frame_preview_orig)
pi_preview_orig = PhotoImage()
l_preview_orig_pi = ttk.Label(frame_preview_orig, image=pi_preview_orig)
b_preview_orig.grid(row=1, column=1, padx=5, pady=5)
l_preview_orig.grid(row=1, column=2, padx=5, pady=5)
l_preview_orig_pi.grid(row=2, column=1, columnspan=2)

###########################
# Histogram original
###########################
frame_histogram_orig = ttk.LabelFrame(frame_second_col, text=_("Histogram"))
frame_histogram_orig.grid(row=3, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
pi_histogram_orig = PhotoImage()
l_histogram_orig = ttk.Label(frame_histogram_orig, image=pi_histogram_orig)
l_histogram_orig.grid(row=1, column=1, padx=10, pady=5)

#####################################################
# Third column
#####################################################
frame_third_col = ttk.Frame(main)
frame_third_col.grid(row=1, column=4, sticky=(N, W, E, S))

##########################
# Apply all
##########################
frame_apply = ttk.LabelFrame(frame_third_col,
                             text=_("Apply"),
                             style="Blue.TLabelframe")
frame_apply.grid(row=1, column=1, sticky=(N, W, E, S), padx=5, pady=5)

rb_apply_dir = ttk.Radiobutton(frame_apply, text=_("Folder"),
                               variable=file_dir_selector,
                               value="1")
rb_apply_file = ttk.Radiobutton(frame_apply, text=_("File"),
                                variable=file_dir_selector,
                                value="0")
b_apply = ttk.Button(frame_apply,
                     text=_("Apply all"),
                     command=apply_all_button,
                     style="Blue.TButton")

rb_apply_dir.grid(column=1, row=1, padx=5, pady=5, sticky=W)
rb_apply_file.grid(column=2, row=1, padx=5, pady=5, sticky=W)
b_apply.grid(column=3, row=1, padx=5, pady=5, sticky=(W, E))

##########################
# ProgressBar
#########################
pb = ttk.Progressbar(frame_apply, orient="horizontal",
                     mode="determinate",
                     var=progress_var)
pb['value'] = 0
pb.grid(row=2, column=1, columnspan=3, padx=5, sticky=(W, E))

l_pb = ttk.Label(frame_apply, textvariable=progress_files)
l_pb.grid(row=3, column=1, columnspan=3, padx=5, pady=2, sticky=W)

##########################
# Result preview
###########################
frame_preview_new = ttk.Labelframe(frame_third_col,
                                   text=_("Result"),
                                   style="Blue.TLabelframe")
frame_preview_new.grid(row=3, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
b_preview_new = ttk.Button(frame_preview_new,
                           text=_("Preview"),
                           command=preview_new_button)
l_preview_new = ttk.Label(frame_preview_new)
pi_preview_new = PhotoImage()
l_preview_new_pi = ttk.Label(frame_preview_new, image=pi_preview_new)
# c_preview_new_pi = Canvas(frame_preview_new, width=300, height=300)
b_preview_new.grid(row=1, column=1, padx=5, pady=5)
l_preview_new.grid(row=1, column=2, padx=5, pady=5)
l_preview_new_pi.grid(row=2, column=1, columnspan=2)
# c_preview_new_pi.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

###########################
# Histogram new
###########################
frame_histogram_new = ttk.LabelFrame(frame_third_col, text=_("Histogram"))
frame_histogram_new.grid(row=4, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
pi_histogram_new = PhotoImage()
l_histogram_new = ttk.Label(frame_histogram_new, image=pi_histogram_new)
l_histogram_new.grid(row=1, column=1, padx=10, pady=5)


###############################################################################
# bind
###############################################################################

# binding commands to widgets
cb_text_font.bind("<<ComboboxSelected>>", font_selected)
cb_contrast.bind("<<ComboboxSelected>>", contrast_selected)
l_preview_orig_pi.bind("<Button-1>", mouse_crop_NW)
l_preview_orig_pi.bind("<Button-3>", mouse_crop_SE)
# rb0_crop.bind("<Button-1>", preview_orig_bind)
rb1_crop.bind("<ButtonRelease-1>", preview_orig_bind)
rb2_crop.bind("<ButtonRelease-1>", preview_orig_bind)
rb3_crop.bind("<Button-1>", preview_orig_bind)
root.bind("<F1>", help_info)
root.protocol("WM_DELETE_WINDOW", win_deleted)

##########################################
# Run functions
#
ini_read_wraper()  # Loading from config file
fonts()    # Reading available fonts
no_text_in_windows()  # Warning if Windows
tools_set()
if os.path.isfile(file_in_path.get()):
    # Load preview picture
    preview_orig()
if os.path.isfile(file_logo_path.get()):
    # Load preview logo
    preview_logo()

l_border.configure(bg=img_border_color.get())

root.mainloop()

# EOF
