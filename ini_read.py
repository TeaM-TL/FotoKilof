# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" moduł z funkcją odczytu awartości pliku konfiguracyjnego ini """

import configparser
import platform

def ini_read(file_ini):
    """ Obsługa pliku konfiguracyjnego INI """

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
    dict_return['img_histograms'] = histograms

    try:
        resize = config.getint('Resize', 'resize')
    except:
        resize = "1"
    dict_return['img_resize'] = resize

    try:
        resize_size_pixel = config.getint('Resize', 'size_pixel')
    except:
        resize_size_pixel = "0"
    dict_return['resize_size_pixel'] = resize_size_pixel

    try:
        resize_size_percent = config.getint('Resize', 'size_percent')
    except:
        resize_size_percent = "0"
    dict_return['resize_size_pixel'] = resize_size_percent

    try:
        text_on = config.getint('Text', 'on')
    except:
        text_on = "1"
    dict_return['img_text'] = text_on

    try:
        text = config.get('Text', 'text')
    except:
        text = ""
    dict_return['img_text_text'] = text

    try:
        text_gravity = config.get('Text', 'gravity')
    except:
        text_gravity = "SE"
    dict_return['img_text_gravity'] = text_gravity

    if platform.system() == "Windows":
        text_font = "Arial"
    else:
        try:
            text_font = config.get('Text', 'font')
        except:
            text_font = "Helvetica"
    dict_return['img_text_font'] = text_font

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
    dict_return['img_text_color'] = text_color

    try:
        text_box = config.getint('Text', 'box')
    except:
        text_box = 0
    dict_return['img_text_box'] = text_box

    try:
        text_box_color = config.get('Text', 'box_color')
    except:
        text_box_color = "#000000"
    dict_return['img_text_box_color'] = text_box_color

    try:
        rotate = config.getint('Rotate', 'rotate')
    except:
        rotate = "0"
    dict_return['img_rotate'] = rotate

    try:
        crop = config.getint('Crop', 'crop')
    except:
        crop = "0"
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
        crop_2_X = config.getint('Crop', '2_X')
    except:
        crop_2_X = "0"
    dict_return['crop_2_X'] = crop_2_X

    try:
        crop_2_Y = config.getint('Crop', '2_Y')
    except:
        crop_2_Y = "0"
    dict_return['crop_2_Y'] = crop_2_Y

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
        crop_3_X = config.getint('Crop', '3_X')
    except:
        crop_3_X = "0"
    dict_return['crop_3_X'] = crop_3_X

    try:
        crop_3_Y = config.getint('Crop', '3_Y')
    except:
        crop_3_Y = "0"
    dict_return['crop_3_Y'] = crop_3_Y

    try:
        crop_gravity = config.getint('Crop', 'gravity')
    except:
        crop_gravity = "C"
    dict_return['img_crop_gravity'] = crop_gravity

    try:
        border_color = config.get('Border', 'color')
    except:
        border_color = "#FFFFFF"
    dict_return['img_border_color'] = border_color

    try:
        border = config.getint('Border', 'size')
    except:
        border = "0"
    dict_return['img_border_size'] = border

    try:
        normalize = config.getint('Color', 'normalize')
    except:
        normalize = 0
    dict_return['img_normalize'] = normalize

    try:
        black_white = config.getint('Color', 'bw')
    except:
        black_white = 0
    dict_return['img_bw'] = black_white

    try:
        bw_sepia = config.getint('Color', 'sepia')
    except:
        bw_sepia = "95"
    dict_return['img_sepia'] = bw_sepia

    try:
        contrast = config.getint('Contrast', 'contrast')
    except:
        contrast = "0"
    dict_return['img_contrast'] = contrast

    try:
        contrast_stretch_1 = config.get('Contrast', 'stretch1')
    except:
        contrast_stretch_1 = "0.15"
    dict_return['img_contrast_stretch_1'] = contrast_stretch_1

    try:
        contrast_stretch_2 = config.get('Contrast', 'stretch2')
    except:
        contrast_stretch_2 = "0.05"
    dict_return['img_contrast_stretch_2'] = contrast_stretch_2

    return dict_return

# EOF
