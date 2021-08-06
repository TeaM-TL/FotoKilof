# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=bare-except

"""
Copyright (c) 2019-2021 Tomasz Łuczak, TeaM-TL

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

nice GUI for ImageMagick command common used (by me)
"""

import configparser
import datetime
import gettext
import os
import re
import sys
import tempfile

from tkinter import Tk, ttk, Label, PhotoImage, PanedWindow
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from tkinter import TclError, StringVar, IntVar
from tkinter import N, S, W, E, END, DISABLED, NORMAL

try:
    from tkcolorpicker import askcolor
except:
    from tkinter.colorchooser import askcolor

import mswindows
if mswindows.windows() == 1:
    from PIL import ImageGrab

# my modules
import convert
import common
import gui
import ini_read
import log
import magick
import preview

# Start logging
log.write_log('Start', "M", "w", 1)

# set locale for Windows
if mswindows.windows() == 1:
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
if not os.path.isdir(localedir):
    localedir = os.path.join(os.getcwd(), 'locale')
translate_info = str("Locale directory: " + localedir)
log.write_log(translate_info, "M")

translate = gettext.translation('fotokilof', localedir, fallback=True)
gettext.install('fotokilof', localedir)
_ = translate.gettext

translate_info = str(gettext.find('base', 'locales'))
log.write_log(translate_info, "M")

###################
# CONSTANTS
VERSION = "3.7.1"
if mswindows.windows() == 1:
    PREVIEW_ORIG = 400  # preview original
    PREVIEW_NEW = 400  # preview result
    PREVIEW_LOGO = 80  # preview logo
else:
    PREVIEW_ORIG = 450
    PREVIEW_NEW = 450
    PREVIEW_LOGO = 100

preview_size_list = (300, 350, 400, 450, 500, 550, 600, 650, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 1920, 'none')
##########################


def print_command(cmd, cmd_magick):
    """ print command in custom window """
    t_custom.insert(END, cmd + " ")
    # co_custom_command.current(magick_commands.index(cmd_magick))


def convert_custom_clear():
    """ clear custom widget """
    t_custom.delete(1.0, END)

################
# Preview


def preview_orig_clear():
    """ clear every preview if doesn't choose file """
    log.write_log("clear preview", "M")
    l_histogram_orig.configure(image='')
    l_preview_orig_pi.configure(image='')
    # if no original, new previe should be clear too
    preview_new_clear()

def preview_new_clear():
    """ clear every preview if doesn't choose file """
    log.write_log("clear preview", "M")
    l_histogram_new.configure(image='')
    l_preview_new_pi.configure(image='')

def preview_new_refresh(event):
    """ callback after selection of size preview"""

    # to define file_out
    file_out = magick.pre_magick(file_in_path.get(),
                                 os.path.join(work_dir.get(),
                                 work_sub_dir.get()),
                                 co_apply_type.get())
    if os.path.isfile(file_out):
        preview_new(file_out)
    else:
        preview_new_clear()


def preview_new(file_out):
    """ generowanie podglądu wynikowego """

    if co_preview_selector_new.get() != "none":
        preview_info = preview.preview_pillow(file_out,
                                                int(co_preview_selector_new.get()))

        try:
            l_preview_new.configure(text=preview_info['width'] + "x" \
                                + preview_info['height'] \
                                + " - " \
                                + preview_info['size'])
            pi_preview_new.configure(file=preview_info['filename'])
            l_preview_new_pi.configure(image=pi_preview_new)
        except:
            log.write_log("preview_new: Cannot read preview", "E")

        gui.copy_to_clipboard(file_out)

        if img_histograms_on.get() == 1:
            try:
                l_histogram_new.configure(image=pi_histogram_new)
                pi_histogram_new.configure(file=preview.preview_histogram(file_out,
                                                                      GM_or_IM))
            except:
                log.write_log("previe_new: errot in preview histogram_new", "E")
    else:
        preview_new_clear()


def preview_orig_button():
    """ original preview """
    # global file_in_path

    try:
        magick.display_image(file_in_path.get(), GM_or_IM)
    except:
        log.write_log("No orig picture to preview", "W")


def preview_new_button():
    """ preview new picture """

    file_show = os.path.join(os.path.dirname(file_in_path.get()),
                             work_dir.get(),
                             work_sub_dir.get(),
                             os.path.basename(file_in_path.get()))

    try:
        magick.display_image(file_show, GM_or_IM)
    except:
        log.write_log("No new picture to preview", "W")


def extension_from_file():
    """ set extension in ComboBox same as opened file"""
    path = os.path.splitext(file_in_path.get())
    extension = path[1].lower()
    try:
        co_apply_type.current(file_extension.index(extension))
    except:
        log.write_log("extension_from_file: wrong extension", "W")


def apply_all_convert(out_file, write_command):
    """ apply all option together
    write_command = 0 - nothing, 1 - write command into custom widget
    """

    cmd = ""
    text_separate = 0  # all conversion in one run
    previous_command = 0 # if were any command before pip

    if img_normalize_on.get() == 1:
        previous_command = 1
        cmd = cmd + " " + convert.convert_normalize(img_normalize.get(),
                                                    co_normalize_channel.get())

    if img_contrast_on.get() == 1:
        previous_command = 1
        cmd = cmd + " " + convert.convert_contrast(img_contrast.get(),
                                                   co_contrast_selection.get(),
                                                   e1_contrast.get(),
                                                   e2_contrast.get())

    if img_bw_on.get() == 1:
        previous_command = 1
        cmd = cmd + " " + convert.convert_bw(img_bw.get(), e_bw_sepia.get())

    if int(img_resize_on.get()) == 1:
        if img_border_on.get() == 0:
            border = 0
        else:
            border = abs(int(e_border.get()))
        previous_command = 1

        resize = convert.convert_resize(img_resize.get(),
                                        e1_resize.get(),
                                        e2_resize.get(),
                                        border)
        cmd = cmd + " " + resize['command']
    else:
        if int(img_crop_on.get()) == 1:
            previous_command = 1
            if img_text_inout.get() == 0:
                text_separate = 1  # if crop - convert text in second run
            else:
                text_separate = 0  # crop + convert text run together

            cmd = cmd + " " + convert.convert_crop(img_crop.get(),
                                                   img_crop_gravity.get(),
                                                   convert_crop_entries())

    if img_rotate_on.get() > 0:
        previous_command = 1
        cmd = cmd + " " + convert.convert_rotate(img_rotate.get())

    if img_border_on.get() == 1:
        previous_command = 1
        border = int(e_border.get())
        cmd = cmd + " " + convert.convert_border(e_border.get(),
                                                 img_border_color.get(),
                                                 border)

    cmd_magick = GM_or_IM + "convert"
    cmd_text = convert.convert_text(convert_text_entries())

    if text_separate == 0:
        cmd = cmd + " " + cmd_text
        if write_command == 1:
            print_command(cmd, cmd_magick)
        result1 = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
        result2 = "OK"
    else:
        # because text gravity which makes problem with crop gravity
        # we have to force second run of conversion
        if write_command == 1:
            print_command(cmd, cmd_magick)
        result1 = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
        cmd_magick = GM_or_IM + "mogrify"
        if write_command == 1:
            print_command(cmd_text, cmd_magick)
        result2 = magick.magick(cmd_text, "", out_file, cmd_magick)

    if img_logo_on.get() == 1:
        cmd1 = convert.convert_pip(img_logo_gravity.get(),
                                   e_logo_width.get(),
                                   e_logo_height.get(),
                                   e_logo_dx.get(),
                                   e_logo_dy.get()) \
                + " " + common.spacja(file_logo_path.get()) + " "

        if previous_command == 0:
            cmd2 = common.spacja(file_in_path.get())
        else:
            cmd2 = common.spacja(out_file) + " "
        cmd = cmd1 + cmd2
        cmd_magick = GM_or_IM + "composite"
        if write_command == 1:
            print_command(cmd, cmd_magick)

        result3 = magick.magick(cmd, "", out_file, cmd_magick)
    else:
        result3 = None

    if result1 == "OK" or result2 == "OK" or result3 == "OK":
        result = "OK"
    else:
        result = "None"
    return result


def apply_all_button():
    """ all option together, processing one file or whole directory """
    if os.path.isfile(file_in_path.get()):
        progress_files.set(_("Processing"))
        root.update_idletasks()

        # work_sub_dir if will be resize
        if int(img_resize_on.get()) == 1:
            resize = convert.convert_resize(img_resize.get(),
                                            e1_resize.get(),
                                            e2_resize.get(),
                                            0)
            work_sub_dir.set(resize['sub_dir'])
        else:
            work_sub_dir.set("")

        if file_dir_selector.get() == 0:
            out_file = magick.pre_magick(file_in_path.get(),
                                         os.path.join(work_dir.get(),
                                         work_sub_dir.get()),
                                         co_apply_type.get())
            result = apply_all_convert(out_file, 1)
            if result == "OK":
                preview_new(out_file)
        else:
            dirname = os.path.dirname(file_in_path.get())
            i = 0
            files_list_short = common.list_of_images(dirname)
            files_list = []
            for filename_short in files_list_short:
                files_list.append(os.path.join(dirname, filename_short))
            file_list_len = len(files_list)
            for file_in in files_list:
                file_in_path.set(os.path.realpath(file_in))
                out_file = magick.pre_magick(os.path.realpath(file_in),
                                             os.path.join(work_dir.get(),
                                             work_sub_dir.get()),
                                             co_apply_type.get())
                result = apply_all_convert(out_file, 0)
                i = i + 1
                progress_files.set(str(i) + " " + _("of") + " " \
                                   + str(file_list_len) + " : " \
                                   + os.path.basename(file_in))
                progress_var.set(i)
                root.update_idletasks()

            preview_orig()
            if result == "OK":
                preview_new(out_file)

        progress_var.set(0)
        progress_files.set(_("done"))
        root.update_idletasks()
        #work_sub_dir.set("")  # reset subdir name for next processing
    else:
        log.write_log("No file selected", "M")


def convert_custom_button():
    """ execute custom command """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = t_custom.get('1.0', 'end-1c')
    cmd_magick = GM_or_IM + co_custom_command.get()
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))


def convert_contrast_button():
    """ przycisk zmiany kontrastu """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = convert.convert_contrast(int(img_contrast.get()),
                                   co_contrast_selection.get(),
                                   e1_contrast.get(),
                                   e2_contrast.get())
    cmd_magick = GM_or_IM + "convert"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))


def convert_bw_button():
    """ black-white or sepia button """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = convert.convert_bw(img_bw.get(), e_bw_sepia.get())
    cmd_magick = GM_or_IM + "convert"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))


def convert_normalize_button():
    """ normalize button """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = convert.convert_normalize(img_normalize.get(),
                                    co_normalize_channel.get())
    cmd_magick = GM_or_IM + "convert"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))


def convert_rotate_button():
    """ rotate button """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = convert.convert_rotate(img_rotate.get())
    cmd_magick = GM_or_IM + "convert"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))


def convert_resize_button():
    """ Resize button """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    resize= convert.convert_resize(img_resize.get(),
                                   e1_resize.get(),
                                   e2_resize.get(),
                                   '0')
    cmd = resize['command']
    work_sub_dir.set(resize['sub_dir'])

    out_file = magick.pre_magick(file_in_path.get(),
                                 os.path.join(work_dir.get(),
                                              work_sub_dir.get()),
                                 co_apply_type.get())
    cmd_magick = GM_or_IM + "convert"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))
    #work_sub_dir.set("")  # reset subdir name for next processing


def convert_border_button():
    """ Border button """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = convert.convert_border(e_border.get(),
                                 img_border_color.get(),
                                 img_border_on.get())
    cmd_magick = GM_or_IM + "convert"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))


def convert_crop_button():
    """ Crop button """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = convert.convert_crop(img_crop.get(),
                               img_crop_gravity.get(),
                               convert_crop_entries())
    cmd_magick = GM_or_IM + "convert"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))


def convert_logo_button():
    """ Logo button """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = convert.convert_pip(img_logo_gravity.get(),
                              e_logo_width.get(),
                              e_logo_height.get(),
                              e_logo_dx.get(),
                              e_logo_dy.get()) \
          + " " + common.spacja(file_logo_path.get()) \
          + " " + common.spacja(file_in_path.get()) + " "
    cmd_magick = GM_or_IM + "composite"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, "", out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))


def convert_text_button():
    """ przycisk wstawiania tekstu """
    progress_files.set(_("Processing"))
    root.update_idletasks()
    out_file = magick.pre_magick(file_in_path.get(),
                                 work_dir.get(),
                                 co_apply_type.get())
    cmd = convert.convert_text(convert_text_entries())
    cmd_magick = GM_or_IM + "convert"
    print_command(cmd, cmd_magick)
    result = magick.magick(cmd, file_in_path.get(), out_file, cmd_magick)
    if result == "OK":
        preview_new(out_file)
    progress_files.set(_("done"))

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
    dict_return['text_inout'] = img_text_inout.get()
    dict_return['text'] = e_text.get()
    dict_return['dx'] = e_text_x.get()
    dict_return['dy'] = e_text_y.get()
    dict_return['gravitation'] = img_text_gravity.get()
    if mswindows.windows() == 1:
        dict_return['font'] = img_text_font_dict[img_text_font.get()]
    else:
        dict_return['font'] = img_text_font.get()
    dict_return['font_size'] = e_text_size.get()
    dict_return['text_color'] = img_text_color.get()
    dict_return['box'] = img_text_box.get()
    dict_return['box_color'] = img_text_box_color.get()
    return dict_return


def fonts():
    """ preparing font names for ImageMagick """

    result = magick.get_fonts_dict(GM_or_IM)
    co_text_font['values'] = list(result.keys())
    return result

def font_selected(event):
    """ callback via bind for font selection """
    img_text_font.set(co_text_font.get())


def crop_read():
    """ Wczytanie rozmiarów z obrazka do wycinka """
    img = magick.get_image_size(file_in_path.get(), GM_or_IM)
    width = img[0]
    height = img[1]

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
    if mswindows.windows() == 1:
        filetypes = ((_("All graphics files"), ".JPG .JPEG .PNG .TIF .TIFF"),
                     (_("JPG files"), ".JPG .JPEG"),
                     (_("PNG files"), ".PNG"),
                     (_("TIFF files"), ".TIF .TIFF"),
                     (_("SVG files"), ".SVG"),
                     (_("ALL types"), "*"))
    else:
        filetypes = ((_("All graphics files"), ".JPG .jpg .JPEG .jpeg .PNG .png .TIF .tif .TIFF .tiff"),
                     (_("JPG files"), ".JPG .jpg .JPEG .jpeg"),
                     (_("PNG files"), ".PNG .png"),
                     (_("TIFF files"), ".TIF .tif .TIFF .tiff"),
                     (_("SVG files"), ".SVG .svg"),
                     (_("ALL types"), "*"))

    file_logo_path.set(filedialog.askopenfilename(initialdir=directory,
                                                  filetypes=filetypes,
                                                  title=_("Select logo picture for inserting")))
    if os.path.isfile(file_logo_path.get()):
        preview_logo()
    else:
        preview_logo_clear()


def open_file():
    """ open image for processing """
    directory = os.path.dirname(file_in_path.get())

    filetypes = ((_("All graphics files"), ".JPG .jpg .JPEG .jpeg .PNG .png .TIF .tif .TIFF .tiff"),
                 (_("JPG files"), ".JPG .jpg .JPEG .jpeg"),
                 (_("PNG files"), ".PNG .png"),
                 (_("TIFF files"), ".TIF .tif .TIFF .tiff"),
                 (_("SVG files"), ".SVG .svg"),
                 (_("ALL types"), "*"))
    result = filedialog.askopenfilename(initialdir=directory,
                                        filetypes=filetypes,
                                        title=_("Select picture for processing"))
    if result:
        extension_from_file()
        file_in_path.set(result)
        root.title(window_title + file_in_path.get())
        preview_orig()
    else:
        preview_orig_clear()


def open_file_last_key(event):
    open_file_last()


def open_file_last():
    """ Open last file """
    if file_in_path.get():
        if os.path.isfile(file_in_path.get()):
            cwd = os.path.dirname(file_in_path.get())
            file_list = common.list_of_images(cwd)
            current_file = os.path.basename(file_in_path.get())
            filename = common.file_from_list_of_images(file_list,
                                                   current_file,
                                                   "last")
            if filename is not None:
                try:
                    file_in_path.set(os.path.normpath(os.path.join(cwd, filename)))
                    root.title(window_title + file_in_path.get())
                    preview_orig()
                    extension_from_file()
                    preview_new_refresh("none")
                except:
                    log.write_log("Error in open_file_last", "E")


def open_file_next_key(event):
    open_file_next()


def open_file_next():
    """ Open next file """
    if file_in_path.get():
        if os.path.isfile(file_in_path.get()):
            cwd = os.path.dirname(file_in_path.get())
            file_list = common.list_of_images(cwd)
            current_file = os.path.basename(file_in_path.get())
            filename = common.file_from_list_of_images(file_list,
                                                   current_file,
                                                   "next")
            if filename is not None:
                try:
                    file_in_path.set(os.path.normpath(os.path.join(cwd, filename)))
                    root.title(window_title + file_in_path.get())
                    preview_orig()
                    extension_from_file()
                except:
                    log.write_log("Error in open_file_next", "E")
                try:
                    preview_new_refresh("none")
                except:
                    log.write_log("Error in open_file_next refresh", "E")


def open_file_first_key(event):
    open_file_first()


def open_file_first():
    """ Open first file """
    if file_in_path.get():
        if os.path.isfile(file_in_path.get()):
            cwd = os.path.dirname(file_in_path.get())
            file_list = common.list_of_images(cwd)
            current_file = os.path.basename(file_in_path.get())
            filename = common.file_from_list_of_images(file_list,
                                                   current_file,
                                                   "first")
            if filename is not None:
                try:
                    file_in_path.set(os.path.normpath(os.path.join(cwd, filename)))
                    root.title(window_title + file_in_path.get())
                    preview_orig()
                    extension_from_file()
                    preview_new_refresh("none")
                except:
                    log.write_log("Error in open_file_first", "E")


def open_file_prev_key(event):
    open_file_prev()


def open_file_prev():
    """ Open previous file """
    if file_in_path.get():
        if os.path.isfile(file_in_path.get()):
            cwd = os.path.dirname(file_in_path.get())
            file_list = common.list_of_images(cwd)
            current_file = os.path.basename(file_in_path.get())
            filename = common.file_from_list_of_images(file_list,
                                                   current_file,
                                                   "previous")
            if filename is not None:
                try:
                    file_in_path.set(os.path.normpath(os.path.join(cwd, filename)))
                    root.title(window_title + file_in_path.get())
                    preview_orig()
                except:
                    log.write_log("Error in open_file_first", "E")

                directory = os.path.dirname(file_in_path.get())
                file_in_path.set(os.path.join(directory, filename))
                preview_orig()
                extension_from_file()
                preview_new_refresh("none")


def open_screenshot():
    """ Make screenshot """
    now = datetime.datetime.now()
    today = now.strftime("%F")
    today_dir = os.path.join(tempfile.gettempdir(), today)
    if not os.path.isdir(today_dir):
        try:
            os.mkdir(today_dir)
        except:
            log.write_log("Error in open_screenshot, make today directory", "E")

    filename = now.strftime("%F_%H-%M-%S_%f") + ".png"
    out_file = os.path.join(today_dir, filename)
    if mswindows.windows() == 1:
        screenshot = ImageGrab.grabclipboard()
        try:
            screenshot.save(out_file, 'PNG')
        except:
            log.write_log('Error in open_screenshot, save from clipboards', 'E')
    else:
        magick.magick(" ", "-quiet", out_file, "import")
    file_in_path.set(out_file)
    root.title(window_title + out_file)
    preview_orig()
    extension_from_file()
    preview_new_refresh("none")


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
        color = askcolor(img_text_color.get())
        if color[1] is None:
            img_text_box_color.set("#FFFFFF")
        else:
            img_text_box_color.set(color[1])
            l_text_font_selected.configure(bg=img_text_box_color.get())


def color_choose():
    """ Color selection """
    color = askcolor(img_text_color.get())
    if color[1] is None:
        img_text_color.set("#FFFFFF")
    else:
        img_text_color.set(color[1])
    l_text_font_selected.configure(fg=img_text_color.get())


def ini_read_wraper():
    """ Read config INI file """

    ini_entries = ini_read.ini_read(FILE_INI, theme_list, preview_size_list)
    file_in_path.set(ini_entries['file_in_path'])
    file_dir_selector.set(ini_entries['file_dir_selector'])
    work_dir.set(ini_entries['work_dir'])
    img_histograms_on.set(ini_entries['img_histograms_on'])
    co_theme_selector.current(theme_list.index(ini_entries['theme']))
    co_preview_selector_orig.current(preview_size_list.index(ini_entries['preview_orig']))
    co_preview_selector_new.current(preview_size_list.index(ini_entries['preview_new']))
    log_level.set(ini_entries['log_level'])

    ini_entries = ini_read.ini_read_resize(FILE_INI)
    img_resize_on.set(ini_entries['img_resize_on'])
    img_resize.set(ini_entries['img_resize'])
    e1_resize.delete(0, "end")
    e1_resize.insert(0, ini_entries['resize_size_pixel'])
    e2_resize.delete(0, "end")
    e2_resize.insert(0, ini_entries['resize_size_percent'])

    ini_entries = ini_read.ini_read_text(FILE_INI, img_text_font_dict)
    img_text_on.set(ini_entries['img_text_on'])
    img_text_inout.set(ini_entries['img_text_inout'])
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

    ini_entries = ini_read.ini_read_normalize(FILE_INI, normalize_channels)
    img_normalize_on.set(ini_entries['normalize_on'])
    img_normalize.set(ini_entries['normalize'])
    co_normalize_channel.current(normalize_channels.index(ini_entries['channel']))

    ini_entries = ini_read.ini_read_contrast(FILE_INI, contrast_selection)
    img_contrast_on.set(ini_entries['contrast_on'])
    img_contrast.set(ini_entries['contrast'])
    co_contrast_selection.current(contrast_selection.index(ini_entries['contrast_selection']))
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
    config.set('Konfiguracja', 'theme', co_theme_selector.get())
    config.set('Konfiguracja', 'preview_orig', co_preview_selector_orig.get())
    config.set('Konfiguracja', 'preview_new', co_preview_selector_new.get())
    config.set('Konfiguracja', 'log', log_level.get())
    config.add_section('Resize')
    config.set('Resize', 'on', str(img_resize_on.get()))
    config.set('Resize', 'resize', str(img_resize.get()))
    config.set('Resize', 'size_pixel', e1_resize.get())
    config.set('Resize', 'size_percent', e2_resize.get())
    config.add_section('Text')
    config.set('Text', 'on', str(img_text_on.get()))
    config.set('Text', 'inout', str(img_text_inout.get()))
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
    config.set('Normalize', 'channel', co_normalize_channel.get())
    config.add_section('Contrast')
    config.set('Contrast', 'on', str(img_contrast_on.get()))
    config.set('Contrast', 'contrast', str(img_contrast.get()))
    config.set('Contrast', 'selection', co_contrast_selection.get())
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
        log.write_log("ini_save: cannot save config file: " + FILE_INI, "E")


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
        log.write_log("help_info: error during loading license file", "W")
        message = "Copyright 2019-2021 Tomasz Łuczak under MIT license"

    messagebox.showinfo(title=_("License"), message=message)


def close_window():
    """ close program """
    root.quit()
    root.destroy()
    sys.exit()


def win_deleted():
    """ close program window """
    log.write_log("closed", "M")
    close_window()


def mouse_crop_NW(event):
    """ Left-Upper corner """
    x_preview = event.x
    y_preview = event.y

    xy_max = common.mouse_crop_calculation(file_in_path.get(),
                                           int(co_preview_selector_orig.get()),
                                           GM_or_IM)
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
    xy_max = common.mouse_crop_calculation(file_in_path.get(),
                                           int(co_preview_selector_orig.get()),
                                           GM_or_IM)
    width = int(x_preview*xy_max['x_orig']/xy_max['x_max'])
    height = int(y_preview*xy_max['y_orig']/xy_max['y_max'])
    e3_crop_1.delete(0, "end")
    e3_crop_1.insert(0, width)
    e4_crop_1.delete(0, "end")
    e4_crop_1.insert(0, height)


def preview_orig_refresh(event):
    """ callback after selection of size preview"""
    preview_orig()


def preview_orig():
    """
    generation preview of original picture
    and add crop rectangle
    """
    if co_preview_selector_orig.get() != "none":
        if img_crop_on.get() == 1:
            # draw crop rectangle on preview
            xy_max = common.mouse_crop_calculation(file_in_path.get(),
                                               int(co_preview_selector_orig.get()),
                                               GM_or_IM)
            if img_crop.get() == 1:
                x0 = int(e1_crop_1.get())
                y0 = int(e2_crop_1.get())
                x1 = int(e3_crop_1.get())
                y1 = int(e4_crop_1.get())
                # do_nothing = 0
            elif img_crop.get() == 2:
                x0 = int(e1_crop_2.get())
                y0 = int(e2_crop_2.get())
                x1 = x0 + int(e3_crop_2.get())
                y1 = y0 + int(e4_crop_2.get())
                # do_nothing = 0
            elif img_crop.get() == 3:
                coord_for_crop = (int(e1_crop_3.get()), int(e2_crop_3.get()),
                              int(e3_crop_3.get()), int(e4_crop_3.get()),
                              img_crop_gravity.get())
                coord = convert.convert_preview_crop_gravity(coord_for_crop,
                                                         xy_max['x_orig'],
                                                         xy_max['y_orig'])
                x0 = coord[0]
                y0 = coord[1]
                x1 = coord[2]
                y1 = coord[3]
                # do_nothing = 0

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
                                              command,
                                              int(co_preview_selector_orig.get()),
                                              GM_or_IM)
        try:
            pi_preview_orig.configure(file=common.spacja(preview_picture['filename']))
            l_preview_orig_pi.configure(image=pi_preview_orig)
        except:
            log.write_log("preview_orig: Cannot load preview", "E")

        try:
            l_preview_orig.configure(text=preview_picture['width'] + "x" \
                                 + preview_picture['height'] \
                                 + " - " \
                                 + preview_picture['size'])
        except:
            log.write_log("preview_orig: Cannot load image size", "E")

        if img_histograms_on.get() == 1:
            pi_histogram_orig.configure(file=preview.preview_histogram(file_in_path.get(), GM_or_IM))
            l_histogram_orig.configure(image=pi_histogram_orig)
    else:
        preview_orig_clear()


def preview_logo():
    """ generating logo preview """
    if os.path.isfile(file_logo_path.get()):
        l_logo_filename.configure(text=os.path.basename(file_logo_path.get()))

        preview_info = preview.preview_convert(file_logo_path.get(), " ", PREVIEW_LOGO, GM_or_IM)
        # because PIL has problem with coversion RGBA->RGB,
        # is impossible to use command as below :-(
#        preview_info = preview.preview_pillow(file_logo_path.get(), PREVIEW_LOGO)

        try:
            pi_logo_preview.configure(file=preview_info['filename'])
        except:
            log.write_log("Preview_logo: Cannot display file", "E")

        l_logo_preview.configure(text=preview_info['width'] + "x" + preview_info['height'])
    else:
        log.write_log("Preview_logo: Cannot load file", "E")


def preview_logo_clear():
    """ clear if no logo picture is selected """
    l_logo_filename.configure(text=_("No file selected"))
    pi_logo_preview.configure(file="")
    l_logo_preview.configure(text="")


def tools_set():
    """ wybór narzędzi do wyświetlenia """

    if img_custom_on.get() == 1:
        frame_custom.grid()
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

    style.theme_use(co_theme_selector.get())


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
theme_list = style.theme_names()  # read available themes
style.configure("Blue.TButton", foreground="blue")
style.configure("Brown.TButton", foreground="#8B0000")
style.configure("Blue.TLabelframe.Label", foreground="blue")
style.configure("Fiolet.TLabelframe.Label", foreground="#800080")
##########################
# Zmienne globalne

FILE_INI = os.path.join(os.path.expanduser("~"), ".fotokilof.ini")
PWD = os.getcwd()
log_level = StringVar() # E(rror), W(arning), M(essage)
work_dir = StringVar()  # default: "FotoKilof"
work_sub_dir = StringVar()  # subdir for resized pictures
work_sub_dir.set("")  # default none
file_dir_selector = IntVar()
file_in_path = StringVar()  # fullpath original picture
img_histograms_on = IntVar()
img_logo_on = IntVar()  # Logo
file_logo_path = StringVar()  # fullpath logo file
img_logo_gravity = StringVar()
img_resize_on = IntVar()  # Resize
img_resize = IntVar()  # (1, 2, 3, 4, 5)
img_text_on = IntVar()  # Text
img_text_gravity = StringVar()
img_text_font = StringVar()
img_text_font_dict = {}  # dict with available fonts, from fonts()
img_text_color = StringVar()
img_text_box = IntVar()
img_text_box_color = StringVar()
img_text_inout = IntVar()  # Text inside or outside picture
img_rotate_on = IntVar()  # Rotate
img_rotate = IntVar()
img_crop_on = IntVar()  # Crop
img_crop = IntVar()  # (1, 2, 3)
img_crop_gravity = StringVar()
img_border_on = IntVar()  # Border
img_border_color = StringVar()
img_normalize_on = IntVar()  # Normalize
img_normalize = IntVar()  #  (1,2,3)
normalize_channels = ("None", "Red", "Green", "Blue", "Alpha", "Gray", "Cyan", "Magenta", "Yellow", "Black", "Opacity", "Index", "RGB", "RGBA", "CMYK", "CMYKA")
img_bw_on = IntVar()  # Black-white
img_bw = IntVar()
img_contrast_on = IntVar()  # Contrast
img_contrast = IntVar()  # (1, 2)
contrast_selection = ("+3", "+2", "+1", "0", "-1", "-2", "-3")
img_custom_on = IntVar()  # Custom
progress_var = IntVar()  # progressbar
progress_files = StringVar()
file_extension = (".jpeg", ".jpg", ".png", ".tif")
magick_commands = ("composite", "convert")
#magick_commands = ("animate", "compare", "composite", "conjure", "convert",
#                   "identify", "import", "mogrify", "montage", "stream")

######################################################################
# Karty
######################################################################
main_menu = ttk.Frame()
main_tools = ttk.Frame()
main = PanedWindow()

main_menu.pack(side='top', expand=0, fill='both')
main_tools.pack(side='top', expand=0, fill='both')
main.pack(side='bottom', expand=1, fill='both')

validation = main.register(gui.only_numbers)  # Entry validation

####################################################################
# main_menu row
####################################################################

###########################
# Picture selection
###########################
frame_file_select = ttk.Labelframe(main_menu, text=_("Image"),
                                   style="Fiolet.TLabelframe")
frame_file_select.grid(row=1, column=1, sticky=(N, W, E, S), padx=5, pady=5)

b_file_select = ttk.Button(frame_file_select, text=_("File selection"),
                           command=open_file, style="Brown.TButton")

b_file_select_screenshot = ttk.Button(frame_file_select, text=_("Screenshot"),
                                 command=open_screenshot)
if mswindows.windows() == 1:
    b_file_select_screenshot.configure(text=_("Clipboard"))

b_file_select_first = ttk.Button(frame_file_select, text=_("First"),
                                 command=open_file_first)
b_file_select_prev = ttk.Button(frame_file_select, text=_("Previous"),
                                command=open_file_prev)
b_file_select_next = ttk.Button(frame_file_select, text=_("Next"),
                                command=open_file_next)
b_file_select_last = ttk.Button(frame_file_select, text=_("Last"),
                                command=open_file_last)

b_file_select.grid(column=1, row=1, padx=5, pady=5, sticky=W)
#
b_file_select_screenshot.grid(column=2, row=1, padx=10, pady=5, sticky=W)
#
b_file_select_first.grid(column=5, row=1, padx=5, pady=5, sticky=W)
b_file_select_prev.grid(column=6, row=1, padx=5, pady=5, sticky=W)
b_file_select_next.grid(column=7, row=1, padx=5, pady=5, sticky=W)
b_file_select_last.grid(column=8, row=1, padx=5, pady=5, sticky=W)

##########################
# Apply all
##########################
frame_apply = ttk.LabelFrame(main_menu, text=_("Execute all"),
                             style="Fiolet.TLabelframe")
frame_apply.grid(row=1, column=2, sticky=(N, W, E, S), padx=5, pady=5)

rb_apply_dir = ttk.Radiobutton(frame_apply, text=_("Folder"),
                               variable=file_dir_selector, value="1")
rb_apply_file = ttk.Radiobutton(frame_apply, text=_("File"),
                                variable=file_dir_selector, value="0")
co_apply_type = ttk.Combobox(frame_apply, width=4, values=file_extension)
co_apply_type.configure(state='readonly')
co_apply_type.current(file_extension.index(".jpg"))
b_apply_run = ttk.Button(frame_apply, text=_("Execute all"),
                         command=apply_all_button,
                         style="Brown.TButton")

b_apply_run.grid(row=1, column=1, padx=5, pady=5, sticky=(W, E))
rb_apply_dir.grid(row=1, column=2, pady=5, sticky=W)
rb_apply_file.grid(row=1, column=3, padx=5, pady=5, sticky=W)

co_apply_type.grid(row=1, column=4, padx=5, pady=1, sticky=(W, E))

l_pb = ttk.Label(frame_apply, textvariable=progress_files, width=35)
l_pb.grid(row=1, column=5, padx=5, pady=2, sticky=W)

###########################
# Buttons
###########################
frame_save = ttk.LabelFrame(main_menu, text=_("Settings"),
                       style="Fiolet.TLabelframe")
frame_save.grid(row=1, column=3, sticky=(N, W, E, S), padx=5, pady=5)

b_last_save = ttk.Button(frame_save, text=_("Save"), command=ini_save)
b_last_read = ttk.Button(frame_save, text=_("Load"), command=ini_read_wraper)

b_last_save.pack(padx=5, pady=1, anchor=W, side='left')
b_last_read.pack(padx=5, pady=1, anchor=W, side='left')

####################################################################
# main_tools row
####################################################################

frame_tools_selection = ttk.Frame(main)

############################
# Tools selection
############################
frame_tools_set = ttk.Labelframe(main_tools, text=_("Tools"),
                                style="Fiolet.TLabelframe")
frame_tools_set.grid(row=1, column=1, padx=5, pady=2, sticky=(W, E))

cb_resize = ttk.Checkbutton(frame_tools_set, text=_("Scaling/Resize"),
                            variable=img_resize_on,
                            offvalue="0", onvalue="1")
cb_crop = ttk.Checkbutton(frame_tools_set, text=_("Crop"),
                          variable=img_crop_on,
                          offvalue="0", onvalue="1")
cb_text = ttk.Checkbutton(frame_tools_set, text=_("Text"),
                          variable=img_text_on,
                          onvalue="1", offvalue="0")
cb_rotate = ttk.Checkbutton(frame_tools_set, text=_("Rotate"),
                            variable=img_rotate_on,
                            offvalue="0", onvalue="1")
cb_border = ttk.Checkbutton(frame_tools_set, text=_("Border"),
                            variable=img_border_on,
                            offvalue="0", onvalue="1")
cb_bw = ttk.Checkbutton(frame_tools_set, text=_("Black&white"),
                        variable=img_bw_on, offvalue="0")
cb_normalize = ttk.Checkbutton(frame_tools_set, text=_("Colors normalize"),
                               variable=img_normalize_on,
                               offvalue="0", onvalue="1")
cb_contrast = ttk.Checkbutton(frame_tools_set, text=_("Contrast"),
                              variable=img_contrast_on,
                              offvalue="0", onvalue="1")
cb_logo = ttk.Checkbutton(frame_tools_set, text=_("Logo"),
                          variable=img_logo_on,
                          offvalue="0", onvalue="1")
cb_custom = ttk.Checkbutton(frame_tools_set, text=_("Custom"),
                            variable=img_custom_on,
                            offvalue="0", onvalue="1")
cb_histograms = ttk.Checkbutton(frame_tools_set, text=_("Histograms"),
                                variable=img_histograms_on,
                                offvalue="0", onvalue="1")

l_theme_selector = ttk.Label(frame_tools_set, text=_("Theme:"))
co_theme_selector = ttk.Combobox(frame_tools_set,
                                 width=9, values=theme_list)
co_theme_selector.configure(state='readonly')

b_layout_set = ttk.Button(frame_tools_set, text=_("Apply"), command=tools_set)

cb_resize.pack(padx=5, pady=1, anchor=W, side='left')
cb_crop.pack(padx=5, pady=1, anchor=W, side='left')
cb_text.pack(padx=5, pady=1, anchor=W, side='left')
cb_rotate.pack(padx=5, pady=1, anchor=W, side='left')
cb_border.pack(padx=5, pady=1, anchor=W, side='left')
cb_bw.pack(padx=5, pady=1, anchor=W, side='left')
cb_contrast.pack(padx=5, pady=1, anchor=W, side='left')
cb_normalize.pack(padx=5, pady=1, anchor=W, side='left')
cb_logo.pack(padx=5, pady=1, anchor=W, side='left')
cb_custom.pack(padx=5, pady=1, anchor=W, side='left')
cb_histograms.pack(padx=5, pady=1, anchor=W, side='left')
b_layout_set.pack(padx=5, pady=1, anchor=W, side='left')
l_theme_selector.pack(padx=5, pady=1, anchor=W, side='left')
co_theme_selector.pack(padx=5, pady=1, anchor=W, side='left')

####################################################################
# main row
####################################################################

#####################################################
# First column
#####################################################
frame_first_col = ttk.Frame(main)

###########################
# Resize
###########################
frame_resize = ttk.Labelframe(frame_first_col, text=_("Scale/Resize"),
                              style="Fiolet.TLabelframe")
frame_resize.grid(column=1, row=2, columnspan=2,
                  sticky=(N, W, E, S), padx=5, pady=5)
###
rb_resize_1 = ttk.Radiobutton(frame_resize, text=_("Pixels"),
                              variable=img_resize, value="1")
e1_resize = ttk.Entry(frame_resize, width=7,
                      validate="key", validatecommand=(validation, '%S'))
rb_resize_2 = ttk.Radiobutton(frame_resize, text=_("Percent"),
                              variable=img_resize, value="2")
e2_resize = ttk.Entry(frame_resize, width=7,
                      validate="key", validatecommand=(validation, '%S'))
rb_resize_3 = ttk.Radiobutton(frame_resize, text="FullHD (1920x1080)",
                              variable=img_resize, value="3")
rb_resize_4 = ttk.Radiobutton(frame_resize, text="2K (2048×1556)",
                              variable=img_resize, value="4")
rb_resize_5 = ttk.Radiobutton(frame_resize, text="4K (4096×3112)",
                              variable=img_resize, value="5")
b_resize_run = ttk.Button(frame_resize, text=_("Execute"),
                          style="Brown.TButton",
                          command=convert_resize_button)

rb_resize_3.grid(row=1, column=1, columnspan=2, sticky=W, padx=5, pady=2)
rb_resize_4.grid(row=1, column=3, columnspan=2, sticky=W, padx=5, pady=2)
rb_resize_5.grid(row=1, column=5, sticky=W, padx=5, pady=2)
rb_resize_1.grid(row=2, column=1, sticky=W, padx=5, pady=5)
e1_resize.grid(row=2, column=2, sticky=W, padx=5, pady=5)
rb_resize_2.grid(row=2, column=3, sticky=W, padx=5, pady=5)
e2_resize.grid(row=2, column=4, sticky=W, padx=5, pady=5)
b_resize_run.grid(row=2, column=5, sticky=(E), padx=5, pady=5)

############################
# crop
############################
frame_crop = ttk.Labelframe(frame_first_col, text=_("Crop"),
                            style="Fiolet.TLabelframe")
frame_crop.grid(row=3, column=1, columnspan=2,
                sticky=(N, W, E, S), padx=5, pady=1)
###
rb1_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="1",
                           text=_("Coordinates (x1, y1) and (x2, y2)"))
f_clickL_crop = ttk.Labelframe(frame_crop, text=_("Left Upper corner"))
l_clickL_crop = ttk.Label(f_clickL_crop, text=_("Click left"))
e1_crop_1 = ttk.Entry(f_clickL_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
e2_crop_1 = ttk.Entry(f_clickL_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
f_clickR_crop = ttk.Labelframe(frame_crop, text=_("Right lower corner"))
l_clickR_crop = ttk.Label(f_clickR_crop, text=_("Click right"))
e3_crop_1 = ttk.Entry(f_clickR_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
e4_crop_1 = ttk.Entry(f_clickR_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))

rb2_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="2",
                           text=_("Origin (x1,y1) and dimensions (X, Y)"))
e1_crop_2 = ttk.Entry(frame_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
e2_crop_2 = ttk.Entry(frame_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
e3_crop_2 = ttk.Entry(frame_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
e4_crop_2 = ttk.Entry(frame_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))

rb3_crop = ttk.Radiobutton(frame_crop, variable=img_crop, value="3",
                           text=_("Offset (dx,dy), dimensions (X, Y)\nand gravity"))
e1_crop_3 = ttk.Entry(frame_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
e2_crop_3 = ttk.Entry(frame_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
e3_crop_3 = ttk.Entry(frame_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))
e4_crop_3 = ttk.Entry(frame_crop, width=4,
                      validate="key", validatecommand=(validation, '%S'))

frame_crop_gravity = ttk.Frame(frame_crop)
rb_crop_NW = ttk.Radiobutton(frame_crop_gravity, text="NW",
                             variable=img_crop_gravity, value="NW")
rb_crop_N = ttk.Radiobutton(frame_crop_gravity, text="N",
                            variable=img_crop_gravity, value="N")
rb_crop_NE = ttk.Radiobutton(frame_crop_gravity, text="NE",
                             variable=img_crop_gravity, value="NE")
rb_crop_W = ttk.Radiobutton(frame_crop_gravity, text="W",
                            variable=img_crop_gravity, value="W")
rb_crop_C = ttk.Radiobutton(frame_crop_gravity, text=_("Center"),
                            variable=img_crop_gravity, value="C")
rb_crop_E = ttk.Radiobutton(frame_crop_gravity, text="E",
                            variable=img_crop_gravity, value="E")
rb_crop_SW = ttk.Radiobutton(frame_crop_gravity, text="SW",
                             variable=img_crop_gravity, value="SW")
rb_crop_S = ttk.Radiobutton(frame_crop_gravity, text="S",
                            variable=img_crop_gravity, value="S")
rb_crop_SE = ttk.Radiobutton(frame_crop_gravity, text="SE",
                             variable=img_crop_gravity, value="SE")
frame_crop_buttons = ttk.Frame(frame_crop)

b_crop_show = ttk.Button(frame_crop_buttons, text=_("Preview"),
                         command=preview_orig)
b_crop_read = ttk.Button(frame_crop_buttons, text=_("From image"),
                         command=crop_read)
b_crop_run = ttk.Button(frame_crop, text=_("Execute"),
                        style="Brown.TButton",
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
rb3_crop.grid(row=4, column=1, sticky=W, padx=5, pady=1)
e1_crop_3.grid(row=4, column=2, sticky=W, padx=10, pady=1)
e2_crop_3.grid(row=4, column=3, sticky=W, padx=5, pady=1)
e3_crop_3.grid(row=4, column=4, sticky=W, padx=5, pady=1)
e4_crop_3.grid(row=4, column=5, sticky=W, padx=5, pady=1)
frame_crop_gravity.grid(row=5, column=4, columnspan=3)
rb_crop_NW.grid(row=1, column=1, sticky=W, pady=1)
rb_crop_N.grid(row=1, column=2, pady=1)
rb_crop_NE.grid(row=1, column=3, sticky=W, pady=1)
rb_crop_W.grid(row=2, column=1, sticky=W, pady=1)
rb_crop_C.grid(row=2, column=2, sticky=W, pady=1)
rb_crop_E.grid(row=2, column=3, sticky=W, pady=1)
rb_crop_SW.grid(row=3, column=1, sticky=W, pady=1)
rb_crop_S.grid(row=3, column=2, pady=1)
rb_crop_SE.grid(row=3, column=3, sticky=W, pady=1)
frame_crop_buttons.grid(row=5, column=1, sticky=(W, E))
b_crop_read.grid(row=1, column=1, sticky=W, padx=15, pady=5)
b_crop_show.grid(row=1, column=2, sticky=W, padx=5, pady=5)
b_crop_run.grid(row=5, column=2, columnspan=2, sticky=W, padx=5, pady=5)


###########################
# Tekst
###########################
frame_text = ttk.Labelframe(frame_first_col, text=_("Add text"),
                            style="Fiolet.TLabelframe")
frame_text.grid(row=4, column=1, columnspan=2,
                sticky=(N, W, E, S), padx=5, pady=1)
###
frame_text_text = ttk.Frame(frame_text)

e_text = ttk.Entry(frame_text_text, width=60)
frame_text_text.grid(row=1, column=1, columnspan=5, sticky=(W, E))
e_text.grid(row=1, column=2, sticky=W, padx=5)
# cb_text_on.grid(row=1, column=3, sticky=W, padx=5)
###
frame_text_xy = ttk.Frame(frame_text)
rb_text_in = ttk.Radiobutton(frame_text_xy, text=_("Inside"),
                             variable=img_text_inout, value="0")
rb_text_out = ttk.Radiobutton(frame_text_xy, text=_("Outside"),
                              variable=img_text_inout, value="1")
l_text_xy = ttk.Label(frame_text_xy, text=_("Offset (dx,dy)\n"))
e_text_x = ttk.Entry(frame_text_xy, width=3,
                     validate="key", validatecommand=(validation, '%S'))
e_text_y = ttk.Entry(frame_text_xy, width=3,
                     validate="key", validatecommand=(validation, '%S'))

frame_text_xy.grid(row=2, column=1, padx=5, pady=2, sticky=(W, N))
rb_text_in.grid(row=1, column=1, sticky=W, padx=5, pady=1)
rb_text_out.grid(row=2, column=1, sticky=W, padx=5, pady=1)
l_text_xy.grid(row=3, column=1, sticky=W, padx=5, pady=1)
e_text_x.grid(row=3, column=2, sticky=(W, N), padx=5, pady=1)
e_text_y.grid(row=3, column=3, sticky=(W, N), padx=5, pady=1)
###
frame_text_gravity = ttk.Frame(frame_text)
rb_text_NW = ttk.Radiobutton(frame_text_gravity, text="NW",
                             variable=img_text_gravity, value="NW")
rb_text_N = ttk.Radiobutton(frame_text_gravity, text="N",
                            variable=img_text_gravity, value="N")
rb_text_NE = ttk.Radiobutton(frame_text_gravity, text="NE",
                             variable=img_text_gravity, value="NE")
rb_text_W = ttk.Radiobutton(frame_text_gravity, text="W",
                            variable=img_text_gravity, value="W")
rb_text_C = ttk.Radiobutton(frame_text_gravity, text=_("Center"),
                            variable=img_text_gravity, value="C")
rb_text_E = ttk.Radiobutton(frame_text_gravity, text="E",
                            variable=img_text_gravity, value="E")
rb_text_SW = ttk.Radiobutton(frame_text_gravity, text="SW",
                             variable=img_text_gravity, value="SW")
rb_text_S = ttk.Radiobutton(frame_text_gravity, text="S",
                            variable=img_text_gravity, value="S")
rb_text_SE = ttk.Radiobutton(frame_text_gravity, text="SE",
                             variable=img_text_gravity, value="SE")
frame_text_gravity.grid(row=2, column=2, columnspan=3, pady=2, sticky=(W, N))
rb_text_NW.grid(row=1, column=1, sticky=W, pady=1)
rb_text_N.grid(row=1, column=2, pady=1)
rb_text_NE.grid(row=1, column=3, sticky=W, pady=1)
rb_text_W.grid(row=2, column=1, sticky=W, pady=1)
rb_text_C.grid(row=2, column=2, pady=1)
rb_text_E.grid(row=2, column=3, sticky=W, pady=1)
rb_text_SW.grid(row=3, column=1, sticky=W, pady=1)
rb_text_S.grid(row=3, column=2, pady=1)
rb_text_SE.grid(row=3, column=3, sticky=W, pady=1)

###
frame_text_font = ttk.Frame(frame_text)
co_text_font = ttk.Combobox(frame_text_font, width=25,
                            textvariable=img_text_font)
co_text_font.configure(state='readonly')
e_text_size = ttk.Entry(frame_text_font, width=3,
                        validate="key", validatecommand=(validation, '%S'))
b_text_color = ttk.Button(frame_text, text=_("Font color"),
                          command=color_choose)
cb_text_box = ttk.Checkbutton(frame_text_font, text=_("Background"),
                              variable=img_text_box,
                              onvalue="1", offvalue="0",
                              command=color_choose_box_active)
b_text_box_color = ttk.Button(frame_text, text=_("Background color"),
                              command=color_choose_box)
b_text_run = ttk.Button(frame_text, text=_("Execute"),
                        style="Brown.TButton", command=convert_text_button)
l_text_font_selected = Label(frame_text, width=20, textvariable=img_text_font)

l_text_font_selected.grid(row=3, column=1, sticky=(W, E), padx=5)
b_text_color.grid(row=3, column=3, sticky=(W, E), padx=5, pady=5)
b_text_box_color.grid(row=3, column=4, sticky=(W, E), padx=5, pady=5)
frame_text_font.grid(row=4, column=1, columnspan=4, sticky=(W, E))
co_text_font.grid(row=1, column=1, sticky=(W, E), padx=5)
e_text_size.grid(row=1, column=2, sticky=W, padx=5)
cb_text_box.grid(row=1, column=3, sticky=W, padx=5)
b_text_run.grid(row=4, column=4, sticky=(W, E), padx=5, pady=5)

###########################
# Rotate
###########################
frame_rotate = ttk.Labelframe(frame_first_col, text=_("Rotate"),
                              style="Fiolet.TLabelframe")
frame_rotate.grid(row=5, column=1, sticky=(N, W, E, S), padx=5, pady=1)
###
rb_rotate_0 = ttk.Radiobutton(frame_rotate, text="0",
                              variable=img_rotate, value="0")
rb_rotate_90 = ttk.Radiobutton(frame_rotate, text="90",
                               variable=img_rotate, value="90")
rb_rotate_180 = ttk.Radiobutton(frame_rotate, text="180",
                                variable=img_rotate, value="180")
rb_rotate_270 = ttk.Radiobutton(frame_rotate, text="270",
                                variable=img_rotate, value="270")
b_rotate_run = ttk.Button(frame_rotate, text=_("Execute"),
                          style="Brown.TButton",
                          command=convert_rotate_button)

rb_rotate_0.grid(row=1, column=1, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_90.grid(row=1, column=2, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_180.grid(row=1, column=3, sticky=(N, W, E, S), padx=5, pady=5)
rb_rotate_270.grid(row=1, column=4, sticky=(N, W, E, S), padx=5, pady=5)
b_rotate_run.grid(row=1, column=5, padx=5, pady=5)

###########################
# Border
###########################
frame_border = ttk.Labelframe(frame_first_col, text=_("Border"),
                              style="Fiolet.TLabelframe")
frame_border.grid(row=6, column=1, sticky=(N, W, E, S), padx=5, pady=1)
###
l_border = Label(frame_border, text=_("Pixels"))
e_border = ttk.Entry(frame_border, width=3,
                     validate="key", validatecommand=(validation, '%S'))
b_border_color = ttk.Button(frame_border, text=_("Color"),
                            command=color_choose_border)
b_border_run = ttk.Button(frame_border, text=_("Execute"),
                          style="Brown.TButton",
                          command=convert_border_button)

l_border.grid(row=1, column=1, padx=5, pady=5)
e_border.grid(row=1, column=2, padx=5, pady=5)
b_border_color.grid(row=1, column=3, padx=5, pady=5)
b_border_run.grid(row=1, column=4, padx=5, pady=5, sticky=E)

############################
# Black-white
############################
frame_bw = ttk.LabelFrame(frame_first_col, text=_("Black-white"),
                          style="Fiolet.TLabelframe")
frame_bw.grid(row=5, column=2, rowspan=2, sticky=(N, E, S), padx=5, pady=1)
###
rb1_bw = ttk.Radiobutton(frame_bw, text=_("Black-white"),
                         variable=img_bw, value="1")
rb2_bw = ttk.Radiobutton(frame_bw, text=_("Sepia"),
                         variable=img_bw, value="2")
e_bw_sepia = ttk.Entry(frame_bw, width=3,
                       validate="key", validatecommand=(validation, '%S'))
l_bw_sepia = ttk.Label(frame_bw, text="%")
b_bw_run = ttk.Button(frame_bw, text=_("Execute"),
                      style="Brown.TButton",
                      command=convert_bw_button)

rb2_bw.grid(row=1, column=1, padx=5, pady=5, sticky=W)
e_bw_sepia.grid(row=1, column=2, padx=5, pady=5, sticky=E)
l_bw_sepia.grid(row=1, column=3, padx=5, pady=5, sticky=W)
rb1_bw.grid(row=2, column=1, padx=5, pady=0, sticky=W)
b_bw_run.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky=E)

########################
# Contrast
#########################
frame_contrast = ttk.Labelframe(frame_first_col, text=_("Contrast"),
                                style="Fiolet.TLabelframe")
frame_contrast.grid(row=7, column=1, sticky=(N, W, E, S), padx=5, pady=1)
###
rb1_contrast = ttk.Radiobutton(frame_contrast, text=_("Stretch"),
                               variable=img_contrast, value="1")
rb2_contrast = ttk.Radiobutton(frame_contrast, text=_("Contrast"),
                               variable=img_contrast, value="2")
co_contrast_selection = ttk.Combobox(frame_contrast, width=3,
                                     values=contrast_selection)
co_contrast_selection.configure(state='readonly')
rb3_contrast = ttk.Radiobutton(frame_contrast, text=_("Normalize"),
                               variable=img_contrast,
                               value="3")
e1_contrast = ttk.Entry(frame_contrast, width=4)
e2_contrast = ttk.Entry(frame_contrast, width=4)
l1_contrast = ttk.Label(frame_contrast, text=_("Black"))
l2_contrast = ttk.Label(frame_contrast, text=_("White"))
b_contrast_run = ttk.Button(frame_contrast, text=_("Execute"),
                            style="Brown.TButton",
                            command=convert_contrast_button)

rb1_contrast.grid(row=1, column=1, padx=5, pady=5, sticky=W)
l1_contrast.grid(row=1, column=2, padx=5, pady=5, sticky=E)
e1_contrast.grid(row=1, column=3, padx=5, pady=5, sticky=E)
l2_contrast.grid(row=1, column=4, padx=5, pady=5, sticky=W)
e2_contrast.grid(row=1, column=5, padx=5, pady=5, sticky=W)
rb2_contrast.grid(row=2, column=1, padx=5, pady=5, sticky=W)
co_contrast_selection.grid(row=2, column=2, padx=5, pady=5, sticky=W)
rb3_contrast.grid(row=3, column=1, padx=5, pady=5, sticky=W)
b_contrast_run.grid(row=3, column=3, padx=5, pady=5, columnspan=3, sticky=E)

############################
# Color normalize
############################
frame_normalize = ttk.LabelFrame(frame_first_col, text=_("Color normalize"),
                                 style="Fiolet.TLabelframe")
frame_normalize.grid(row=7, column=2, sticky=(N, E, S), padx=5, pady=1)
###
rb1_normalize = ttk.Radiobutton(frame_normalize, text=_("Equalize"),
                                variable=img_normalize,
                                value="1")
rb2_normalize = ttk.Radiobutton(frame_normalize, text=_("AutoLevel"),
                                variable=img_normalize,
                                value="2")
l_normalize_channel = ttk.Label(frame_normalize, text=_("Channel:"))
co_normalize_channel = ttk.Combobox(frame_normalize, width=7,
                                    values=normalize_channels)
b_normalize_run = ttk.Button(frame_normalize, text=_("Execute"),
                             style="Brown.TButton",
                             command=convert_normalize_button)

rb1_normalize.grid(row=1, column=1, padx=5, pady=0, sticky=W)
l_normalize_channel.grid(row=1, column=2, padx=5, pady=4, sticky=E)
co_normalize_channel.grid(row=1, column=3, padx=5, pady=4, sticky=E)
rb2_normalize.grid(row=2, column=1, padx=5, pady=4, sticky=W)
b_normalize_run.grid(row=3, column=2, columnspan=2, padx=5, pady=4, sticky=E)

###########################
# Logo
###########################
frame_logo = ttk.Labelframe(frame_first_col, text=_("Logo"),
                            style="Fiolet.TLabelframe")
frame_logo.grid(row=10, column=1, columnspan=2,
                sticky=(N, W, E, S), padx=5, pady=1)

b_logo_select = ttk.Button(frame_logo, text=_("File selection"),
                           command=open_file_logo)

b_logo_run = ttk.Button(frame_logo, text=_("Execute"),
                        command=convert_logo_button,
                        style="Brown.TButton")
l_logo_filename = ttk.Label(frame_logo, width=25)

b_logo_select.grid(row=1, column=1, pady=5)
l_logo_filename.grid(row=1, column=2, padx=5, pady=5, sticky=W)
b_logo_run.grid(row=1, column=3, pady=5, sticky=E)

###
frame_logo_xy = ttk.Frame(frame_logo)
l_logo_XxY = ttk.Label(frame_logo_xy, text=_("Width\nHeight"))
l_logo_dxdy = ttk.Label(frame_logo_xy, text=_("Offset\n(dx,dy)"))
e_logo_width = ttk.Entry(frame_logo_xy, width=3,
                         validate="key", validatecommand=(validation, '%S'))
e_logo_height = ttk.Entry(frame_logo_xy, width=3,
                          validate="key", validatecommand=(validation, '%S'))
e_logo_dx = ttk.Entry(frame_logo_xy, width=3,
                      validate="key", validatecommand=(validation, '%S'))
e_logo_dy = ttk.Entry(frame_logo_xy, width=3,
                      validate="key", validatecommand=(validation, '%S'))

frame_logo_xy.grid(row=2, column=2, padx=5, pady=5)
l_logo_XxY.grid(row=1, column=1, sticky=W, padx=5)
e_logo_width.grid(row=2, column=1, sticky=W, padx=5)
e_logo_height.grid(row=3, column=1, sticky=W, padx=5)
l_logo_dxdy.grid(row=1, column=2, sticky=W, padx=5)
e_logo_dx.grid(row=2, column=2, sticky=W, padx=5)
e_logo_dy.grid(row=3, column=2, sticky=W, padx=5)

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
frame_logo_gravity.grid(row=2, column=3, sticky=E)
rb_logo_NW.grid(row=1, column=1, sticky=W, pady=1)
rb_logo_N.grid(row=1, column=2, pady=1)
rb_logo_NE.grid(row=1, column=3, sticky=W, pady=1)
rb_logo_W.grid(row=2, column=1, sticky=W, pady=1)
rb_logo_C.grid(row=2, column=2, pady=1)
rb_logo_E.grid(row=2, column=3, sticky=W, pady=1)
rb_logo_SW.grid(row=3, column=1, sticky=W, pady=1)
rb_logo_S.grid(row=3, column=2, pady=1)
rb_logo_SE.grid(row=3, column=3, sticky=W, pady=1)

###
frame_logo_preview = ttk.Frame(frame_logo)
frame_logo_preview.grid(row=2, column=1)
pi_logo_preview = PhotoImage()
l_logo_preview_pi = ttk.Label(frame_logo_preview, image=pi_logo_preview)
l_logo_preview = ttk.Label(frame_logo_preview)
l_logo_preview_pi.grid(row=2, column=1, padx=5, pady=1)
l_logo_preview.grid(row=1, column=1, padx=5, pady=1)

############################
# Custom command
############################
frame_custom = ttk.LabelFrame(frame_first_col, text=_("Custom command"),
                              style="Fiolet.TLabelframe")
frame_custom.grid(row=11, column=1, columnspan=2,
                  sticky=(N, W, E, S), padx=5, pady=1)

b_custom_clear = ttk.Button(frame_custom, text=_("Clear"),
                            command=convert_custom_clear)
b_custom_run = ttk.Button(frame_custom, text=_("Execute"),
                          style="Brown.TButton",
                          command=convert_custom_button)

t_custom = ScrolledText(frame_custom, state=NORMAL,
                        height=5, width=45,
                        wrap='word', undo=True)

t_custom.pack(expand=1, fill='both', padx=5, pady=5)
b_custom_run.pack(side='right', padx=5, pady=5)
b_custom_clear.pack(side='right', padx=5, pady=5)

### temporary off, later will be enabled
l_custom_command = ttk.Label(frame_custom, text=_("Command:"))
co_custom_command = ttk.Combobox(frame_custom, width=9,
                                 values=magick_commands)
co_custom_command.current(1)
co_custom_command.configure(state='readonly')

# l_custom_command.grid(row=2, column=1, padx=5, pady=5, sticky=E)
# co_custom_command.grid(row=2, column=2, padx=5, pady=5, sticky=W)


#####################################################
# Second column
#####################################################
frame_second_col = ttk.Frame(main)

############################
# Original preview
############################
frame_preview_orig = ttk.Labelframe(frame_second_col, text=_("Original"),
                                    style="Fiolet.TLabelframe")
frame_preview_orig.grid(row=2, column=1, columnspan=2,
                        sticky=(N, W, E, S), padx=5, pady=5)
###
b_preview_orig_run = ttk.Button(frame_preview_orig, text=_("Preview"),
                                command=preview_orig_button)
l_preview_orig = ttk.Label(frame_preview_orig)
co_preview_selector_orig = ttk.Combobox(frame_preview_orig, width=4,
                                        values=preview_size_list)
co_preview_selector_orig.configure(state='readonly')
pi_preview_orig = PhotoImage()
l_preview_orig_pi = ttk.Label(frame_preview_orig, image=pi_preview_orig)

l_preview_orig_pi.pack(side='bottom')
b_preview_orig_run.pack(side='left', padx=5, pady=5)
l_preview_orig.pack(side='left', padx=5, pady=5)
co_preview_selector_orig.pack(side='left', padx=5, pady=1)

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


##########################
# Result preview
###########################
frame_preview_new = ttk.Labelframe(frame_third_col, text=_("Result"),
                                   style="Fiolet.TLabelframe")
frame_preview_new.grid(row=3, column=1, sticky=(N, W, E, S), padx=5, pady=5)
###
b_preview_new_run = ttk.Button(frame_preview_new, text=_("Preview"),
                               command=preview_new_button)
l_preview_new = ttk.Label(frame_preview_new)
co_preview_selector_new = ttk.Combobox(frame_preview_new, width=4,
                                       values=preview_size_list)
co_preview_selector_new.configure(state='readonly')
pi_preview_new = PhotoImage()
l_preview_new_pi = ttk.Label(frame_preview_new, image=pi_preview_new)

l_preview_new_pi.pack(side='bottom')
b_preview_new_run.pack(side='left', padx=5, pady=5)
l_preview_new.pack(side='left', padx=5, pady=5)
co_preview_selector_new.pack(side='left', padx=5, pady=1)
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
# Add Frames into PanedWindow
###############################################################################
main.add(frame_first_col)
main.add(frame_second_col)
main.add(frame_third_col)

###############################################################################
# bind
###############################################################################
# binding commands to widgets
co_preview_selector_orig.bind("<<ComboboxSelected>>", preview_orig_refresh)
co_preview_selector_new.bind("<<ComboboxSelected>>", preview_new_refresh)
co_text_font.bind("<<ComboboxSelected>>", font_selected)
l_preview_orig_pi.bind("<Button-1>", mouse_crop_NW)
l_preview_orig_pi.bind("<Button-3>", mouse_crop_SE)
root.bind("<F1>", help_info)
root.protocol("WM_DELETE_WINDOW", win_deleted)

root.bind("<Prior>", open_file_prev_key)
root.bind("<Next>", open_file_next_key)
root.bind("<Home>", open_file_first_key)
root.bind("<End>", open_file_last_key)

##########################################
# Run functions
#

# check if [Image|Graphics]Magick is available
GM_or_IM_data = magick.check_magick()
GM_or_IM = GM_or_IM_data[0]
GM_or_IM_name = GM_or_IM_data[1]
GM_or_IM_version = magick.get_magick_version(GM_or_IM)
Python_version = re.findall('^\\d[.]\\d+[.]\\d+', sys.version)
window_title = "Tomasz Łuczak : FotoKilof - " + str(VERSION) + " : " + GM_or_IM_version + " : " + Python_version[0] + " | "
root.title(window_title)
if GM_or_IM is not None:
    img_text_font_dict = fonts()    # Reading available fonts
    ini_read_wraper()  # Loading from config file
    tools_set()
    l_border.configure(bg=img_border_color.get())
    if os.path.isfile(file_in_path.get()):
        root.title(window_title + file_in_path.get())
        # Load preview picture
        preview_orig()
    if img_logo_on.get() == 1:
        if os.path.isfile(file_logo_path.get()):
            # Load preview logo
            preview_logo()

else:
    root.withdraw()
    messagebox.showerror(title=_("Error"),
                         message=_("ImageMagick nor GraphicsMagick are not installed in you system. Is impossile to process any graphics."))
    # disable processing buttons
    b_logo_run.configure(state=DISABLED)
    b_resize_run.configure(state=DISABLED)
    b_crop_read.configure(state=DISABLED)
    b_crop_run.configure(state=DISABLED)
    b_text_run.configure(state=DISABLED)
    b_rotate_run.configure(state=DISABLED)
    b_bw_run.configure(state=DISABLED)
    b_border_run.configure(state=DISABLED)
    b_contrast_run.configure(state=DISABLED)
    b_normalize_run.configure(state=DISABLED)
    b_custom_run.configure(state=DISABLED)
    b_apply_run.configure(state=DISABLED)
    b_preview_orig_run.configure(state=DISABLED)
    b_preview_new_run.configure(state=DISABLED)
    b_file_select_first.configure(state=DISABLED)
    b_file_select_prev.configure(state=DISABLED)
    b_file_select_next.configure(state=DISABLED)
    b_file_select_last.configure(state=DISABLED)
    b_file_select.configure(state=DISABLED)
    b_file_select_screenshot.configure(state=DISABLED)
    root.deiconify()

root.mainloop()

# EOF
