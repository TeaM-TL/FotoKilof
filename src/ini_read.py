# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

"""
moduł z funkcjami odczytu zawartości pliku konfiguracyjnego ini
każda funkcja odczytuje kawałek ini
"""

import configparser
import mswindows


def ini_read(file_ini):
    """ Konfiguracja FotoKilofa """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    # read values from a section
    try:
        file_in = config.get('Konfiguracja', 'path')
    except:
        file_in = ""
    dict_return['file_in_path'] = file_in

    try:
        dir_work = config.get('Konfiguracja', 'work_dir')
    except:
        dir_work = "FotoKilof"
    dict_return['work_dir'] = dir_work

    try:
        file_dir_select = config.getint('Konfiguracja', 'file_dir')
    except:
        file_dir_select = "0"
    dict_return['file_dir_selector'] = file_dir_select

    try:
        histograms = config.getint('Konfiguracja', 'histograms')
    except:
        histograms = "0"
    dict_return['img_histograms_on'] = histograms

    try:
        theme = config.get('Konfiguracja', 'theme')
    except:
        theme = "default"
    dict_return['theme'] = theme

    return dict_return


def ini_read_resize(file_ini):
    """ Skalowanie """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        resize_on = config.getint('Resize', 'on')
    except:
        resize_on = "1"
    dict_return['img_resize_on'] = resize_on

    try:
        resize = config.getint('Resize', 'resize')
    except:
        resize = "3"  # FullHD
    dict_return['img_resize'] = resize

    try:
        resize_size_pixel = config.getint('Resize', 'size_pixel')
    except:
        resize_size_pixel = "1024"
    dict_return['resize_size_pixel'] = resize_size_pixel

    try:
        resize_size_percent = config.getint('Resize', 'size_percent')
    except:
        resize_size_percent = "25"
    dict_return['resize_size_percent'] = resize_size_percent

    return dict_return


def ini_read_text(file_ini):
    """ Konfiguracja FotoKilofa """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        text_on = config.getint('Text', 'on')
    except:
        text_on = "1"
    dict_return['img_text_on'] = text_on

    try:
        text = config.get('Text', 'text')
    except:
        text = ""
    dict_return['text_text'] = text

    try:
        text_gravity = config.get('Text', 'gravity')
    except:
        text_gravity = "SE"
    dict_return['img_text_gravity'] = text_gravity

    if mswindows.windows() == 1:
        text_font = "Arial"
    else:
        try:
            text_font = config.get('Text', 'font')
        except:
            text_font = "Helvetica"
    dict_return['text_font'] = text_font

    try:
        text_size = str(config.getint('Text', 'size'))
    except:
        text_size = 12
    dict_return['text_size'] = text_size

    try:
        text_x = config.getint('Text', 'x')
    except:
        text_x = "5"
    dict_return['text_x'] = text_x

    try:
        text_y = config.getint('Text', 'y')
    except:
        text_y = "5"
    dict_return['text_y'] = text_y

    try:
        text_color = config.get('Text', 'color')
    except:
        text_color = "#FFFFFF"
    dict_return['text_color'] = text_color

    try:
        text_box = config.getint('Text', 'box')
    except:
        text_box = 0
    dict_return['text_box'] = text_box

    try:
        text_box_color = config.get('Text', 'box_color')
    except:
        text_box_color = "#000000"
    dict_return['text_box_color'] = text_box_color

    return dict_return


def ini_read_rotate(file_ini):
    """ Konfiguracja FotoKilofa """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        rotate_on = config.getint('Rotate', 'on')
    except:
        rotate_on = "1"
    dict_return['img_rotate_on'] = rotate_on

    try:
        rotate = config.getint('Rotate', 'rotate')
    except:
        rotate = "90"
    dict_return['img_rotate'] = rotate

    return dict_return


def ini_read_crop(file_ini):
    """ Konfiguracja FotoKilofa """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        crop_on = config.getint('Crop', 'on')
    except:
        crop_on = "0"
    dict_return['img_crop_on'] = crop_on

    try:
        crop = config.getint('Crop', 'crop')
    except:
        crop = "1"
    dict_return['img_crop'] = crop

    try:
        crop_1_x1 = config.getint('Crop', '1_x1')
    except:
        crop_1_x1 = "0"
    dict_return['crop_1_x1'] = crop_1_x1

    try:
        crop_1_y1 = config.getint('Crop', '1_y1')
    except:
        crop_1_y1 = "0"
    dict_return['crop_1_y1'] = crop_1_y1

    try:
        crop_1_x2 = config.getint('Crop', '1_x2')
    except:
        crop_1_x2 = "0"
    dict_return['crop_1_x2'] = crop_1_x2

    try:
        crop_1_y2 = config.getint('Crop', '1_y2')
    except:
        crop_1_y2 = "0"
    dict_return['crop_1_y2'] = crop_1_y2

    try:
        crop_2_x1 = config.getint('Crop', '2_x1')
    except:
        crop_2_x1 = "0"
    dict_return['crop_2_x1'] = crop_2_x1

    try:
        crop_2_y1 = config.getint('Crop', '2_y1')
    except:
        crop_2_y1 = "0"
    dict_return['crop_2_y1'] = crop_2_y1

    try:
        crop_2_width = config.getint('Crop', '2_width')
    except:
        crop_2_width = "0"
    dict_return['crop_2_width'] = crop_2_width

    try:
        crop_2_height = config.getint('Crop', '2_height')
    except:
        crop_2_height = "0"
    dict_return['crop_2_height'] = crop_2_height

    try:
        crop_3_dx = config.getint('Crop', '3_dx')
    except:
        crop_3_dx = "0"
    dict_return['crop_3_dx'] = crop_3_dx

    try:
        crop_3_dy = config.getint('Crop', '3_dy')
    except:
        crop_3_dy = "0"
    dict_return['crop_3_dy'] = crop_3_dy

    try:
        crop_3_width = config.getint('Crop', '3_width')
    except:
        crop_3_width = "0"
    dict_return['crop_3_width'] = crop_3_width

    try:
        crop_3_height = config.getint('Crop', '3_height')
    except:
        crop_3_height = "0"
    dict_return['crop_3_height'] = crop_3_height

    try:
        crop_gravity = config.getint('Crop', 'gravity')
    except:
        crop_gravity = "C"
    dict_return['img_crop_gravity'] = crop_gravity

    return dict_return


def ini_read_border(file_ini):
    """ Konfiguracja FotoKilofa """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        border_on = config.get('Border', 'on')
    except:
        border_on = "1"
    dict_return['img_border_on'] = border_on

    try:
        border_color = config.get('Border', 'color')
    except:
        border_color = "#FFFFFF"
    dict_return['img_border_color'] = border_color

    try:
        border = config.getint('Border', 'size')
    except:
        border = "10"
    dict_return['img_border_size'] = border

    return dict_return


def ini_read_color(file_ini):
    """ Konfiguracja FotoKilofa """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        color_on = config.getint('Color', 'on')
    except:
        color_on = "1"
    dict_return['color_on'] = color_on

    try:
        black_white = config.getint('Color', 'black-white')
    except:
        black_white = "1"
    dict_return['black_white'] = black_white

    try:
        bw_sepia = config.getint('Color', 'sepia')
    except:
        bw_sepia = "95"
    dict_return['sepia'] = bw_sepia

    return dict_return


def ini_read_normalize(file_ini):
    """ Normalize """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        normalize_on = config.getint('Normalize', 'on')
    except:
        normalize_on = 0
    dict_return['normalize_on'] = normalize_on

    try:
        normalize = config.getint('Normalize', 'normalize')
    except:
        normalize = 1
    dict_return['normalize'] = normalize

    return dict_return


def ini_read_contrast(file_ini):
    """ Konfiguracja FotoKilofa """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        contrast_on = config.getint('Contrast', 'on')
    except:
        contrast_on = "0"
    dict_return['contrast_on'] = contrast_on

    try:
        contrast = config.getint('Contrast', 'contrast')
    except:
        contrast = "1"
    dict_return['contrast'] = contrast

    try:
        contrast_selection = config.get('Contrast', 'selection')
    except:
        contrast_selection = "0"
    dict_return['contrast_selection'] = contrast_selection

    try:
        contrast_stretch_1 = config.get('Contrast', 'stretch1')
    except:
        contrast_stretch_1 = "0.15"
    dict_return['contrast_stretch_1'] = contrast_stretch_1

    try:
        contrast_stretch_2 = config.get('Contrast', 'stretch2')
    except:
        contrast_stretch_2 = "0.05"
    dict_return['contrast_stretch_2'] = contrast_stretch_2

    return dict_return


def ini_read_logo(file_ini):
    """ Logo cofiguration """

    # słownik wyjściowy
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        logo_on = config.getint('Logo', 'on')
    except:
        logo_on = 0
    dict_return['img_logo_on'] = logo_on

    try:
        logo = config.get('Logo', 'logo')
    except:
        logo = ""
    dict_return['logo_logo'] = logo

    try:
        logo_gravity = config.get('Logo', 'gravity')
    except:
        logo_gravity = "SE"
    dict_return['img_logo_gravity'] = logo_gravity

    try:
        logo_width = config.getint('Logo', 'width')
    except:
        logo_width = "100"
    dict_return['logo_width'] = logo_width

    try:
        logo_height = config.getint('Logo', 'height')
    except:
        logo_height = "100"
    dict_return['logo_height'] = logo_height

    try:
        logo_dx = config.getint('Logo', 'dx')
    except:
        logo_dx = "5"
    dict_return['logo_dx'] = logo_dx

    try:
        logo_dy = config.getint('Logo', 'dy')
    except:
        logo_dy = "5"
    dict_return['logo_dy'] = logo_dy

    return dict_return


def ini_read_custom(file_ini):
    """ Custom """

    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        custom_on = config.getint('Custom', 'on')
    except:
        custom_on = 0
    dict_return['custom_on'] = custom_on

    return dict_return


# EOF
