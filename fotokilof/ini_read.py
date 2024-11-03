# -*- coding: utf-8 -*-
# pylint: disable=bare-except
# pylint: disable=too-many-branches

"""
Copyright (c) 2019-2024 Tomasz Łuczak, TeaM-TL

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

module contains function for reading entries from config file.
Every function read part of config file
- ini_read - general setting for FotoKilof
- resize
- text
- rotate
- crop
- border
- vignette
- color
- normalize
- contrast
- logo
- compose
"""

import configparser

import entries
import common


def main(file_ini, preview_size_list):
    """General settings"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    # read values from a section
    try:
        file_in = config.get("Main", "path")
    except:
        file_in = ""
    dict_return["file_in_path"] = file_in

    try:
        dir_work = config.get("Main", "work_dir")
    except:
        dir_work = "FotoKilof"
    dict_return["work_dir"] = dir_work

    try:
        file_dir_select = config.getint("Main", "file_dir")
    except:
        file_dir_select = "0"
    dict_return["file_dir_selector"] = entries.parse_list(file_dir_select, (0, 1), 0)

    try:
        exif = config.getint("Main", "exif")
    except:
        exif = "0"
    dict_return["img_exif_on"] = entries.parse_list(exif, (0, 1), 0)

    try:
        custom = config.getint("Main", "custom")
    except:
        custom = 0
    dict_return["img_custom_on"] = entries.parse_list(custom, (0, 1), 0)

    try:
        preview_orig = config.getint("Main", "preview_orig")
    except:
        preview_orig = 400
    dict_return["preview_orig"] = entries.parse_list(
        preview_orig, preview_size_list, 400
    )

    try:
        preview_new = config.getint("Main", "preview_new")
    except:
        preview_new = 400
    dict_return["preview_new"] = entries.parse_list(preview_new, preview_size_list, 400)

    try:
        log_level = config.get("Main", "log_level")
    except:
        log_level = "E"
    dict_return["log_level"] = entries.parse_list(log_level, ("E", "W", "I", "D"), "W")

    try:
        check_version = config.getint("Main", "check_version")
    except:
        check_version = 1
    dict_return["check_version"] = entries.parse_list(check_version, (0, 1), 0)

    return dict_return


def resize(file_ini):
    """Resize/scalling"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        resize_on = config.getint("Resize", "on")
    except:
        resize_on = "0"
    dict_return["img_resize_on"] = entries.parse_list(resize_on, (0, 1), 0)

    try:
        resize_variant = config.getint("Resize", "resize")
    except:
        resize_variant = "3"  # FullHD
    dict_return["img_resize"] = entries.parse_list(resize_variant, (1, 2, 3, 4, 5), 3)

    try:
        resize_size_pixel_x = config.getint("Resize", "size_pixel_x")
    except:
        resize_size_pixel_x = "1024"
    dict_return["resize_size_pixel_x"] = resize_size_pixel_x

    try:
        resize_size_pixel_y = config.getint("Resize", "size_pixel_y")
    except:
        resize_size_pixel_y = "1024"
    dict_return["resize_size_pixel_y"] = resize_size_pixel_y

    try:
        resize_size_percent = config.getint("Resize", "size_percent")
    except:
        resize_size_percent = "25"
    dict_return["resize_size_percent"] = resize_size_percent

    return dict_return


def text(file_ini, fonts_dict, operating_system):
    """Text configuration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        text_on = config.getint("Text", "on")
    except:
        text_on = "0"
    dict_return["img_text_on"] = entries.parse_list(text_on, (0, 1), 0)

    try:
        text_inout = config.getint("Text", "inout")
    except:
        text_inout = "1"
    dict_return["img_text_inout"] = entries.parse_list(text_inout, (0, 1), 1)

    try:
        text_string = config.get("Text", "text")
    except:
        text_string = ""
    dict_return["text_text"] = text_string

    try:
        text_gravity = config.get("Text", "gravity")
    except:
        text_gravity = "SE"
    dict_return["img_text_gravity"] = entries.parse_list(
        text_gravity, ("NW", "N", "NE", "W", "C", "E", "SW", "S", "SE"), "SE"
    )

    try:
        text_gravity_onoff = config.getint("Text", "gravity_onoff")
    except:
        text_gravity_onoff = "1"
    dict_return["img_text_gravity_onoff"] = entries.parse_list(
        text_gravity_onoff, (0, 1), 1
    )

    if operating_system == 'Windows':
        default_font = "Arial"
    elif operating_system == 'MACOS':
        default_font = "Helvetica"
    else:
        default_font = "DejaVu-Sans"
    try:
        text_font = config.get("Text", "font")
    except:
        text_font = default_font
    dict_return["text_font"] = entries.parse_list(text_font, fonts_dict, default_font)

    try:
        text_size = str(config.getint("Text", "size"))
    except:
        text_size = 12
    dict_return["text_size"] = text_size

    try:
        text_x = config.getint("Text", "x")
    except:
        text_x = "5"
    dict_return["text_x"] = text_x

    try:
        text_y = config.getint("Text", "y")
    except:
        text_y = "5"
    dict_return["text_y"] = text_y

    try:
        text_color = config.get("Text", "color")
    except:
        text_color = "#FFFFFF"
    dict_return["text_color"] = entries.parse_color(text_color, "#FFFFFF")

    try:
        text_box = config.getint("Text", "box")
    except:
        text_box = 0
    dict_return["text_box"] = entries.parse_list(text_box, (0, 1), 0)

    try:
        text_box_color = config.get("Text", "box_color")
    except:
        text_box_color = "#000000"
    dict_return["text_box_color"] = entries.parse_color(text_box_color, "#000000")

    try:
        text_rotate = config.getint("Text", "text_rotate")
    except:
        text_rotate = "0"
    dict_return["text_rotate"] = entries.parse_list(
        text_rotate, (-1, 0, 90, 180, 270), 0
    )

    try:
        rotate_own = config.getint("Text", "text_rotate_own")
    except:
        rotate_own = "0"
    dict_return["text_rotate_own"] = str(common.empty(rotate_own))

    try:
        text_arrow = config.getint("Text", "text_arrow")
    except:
        text_arrow = "0"
    dict_return["text_arrow"] = entries.parse_list(
        text_arrow, (0, 1), 0
    )

    return dict_return


def rotate(file_ini):
    """Rotate configuration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        rotate_on = config.getint("Rotate", "on")
    except:
        rotate_on = "0"
    dict_return["img_rotate_on"] = entries.parse_list(rotate_on, (0, 1), 0)

    try:
        rotate_variant = config.getint("Rotate", "rotate")
    except:
        rotate_variant = "90"
    dict_return["img_rotate"] = entries.parse_list(rotate_variant, (0, 90, 180, 270), 0)

    try:
        rotate_own = config.getint("Rotate", "own")
    except:
        rotate_own = "0"
    dict_return["img_rotate_own"] = str(common.empty(rotate_own))

    try:
        rotate_color = config.get("Rotate", "color")
    except:
        rotate_color = "#FFFFFF"
    dict_return["img_rotate_color"] = entries.parse_color(rotate_color, "#FFFFFF")

    return dict_return


def crop(file_ini):
    """Crop configuration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        crop_on = config.getint("Crop", "on")
    except:
        crop_on = "0"
    dict_return["img_crop_on"] = entries.parse_list(crop_on, (0, 1), 0)

    try:
        crop_variant = config.getint("Crop", "crop")
    except:
        crop_variant = "1"
    dict_return["img_crop"] = entries.parse_list(crop_variant, (1, 2, 3), 1)

    try:
        crop_1_x1 = config.getint("Crop", "1_x1")
    except:
        crop_1_x1 = "0"
    dict_return["crop_1_x1"] = crop_1_x1

    try:
        crop_1_y1 = config.getint("Crop", "1_y1")
    except:
        crop_1_y1 = "0"
    dict_return["crop_1_y1"] = crop_1_y1

    try:
        crop_1_x2 = config.getint("Crop", "1_x2")
    except:
        crop_1_x2 = "0"
    dict_return["crop_1_x2"] = crop_1_x2

    try:
        crop_1_y2 = config.getint("Crop", "1_y2")
    except:
        crop_1_y2 = "0"
    dict_return["crop_1_y2"] = crop_1_y2

    try:
        crop_2_x1 = config.getint("Crop", "2_x1")
    except:
        crop_2_x1 = "0"
    dict_return["crop_2_x1"] = crop_2_x1

    try:
        crop_2_y1 = config.getint("Crop", "2_y1")
    except:
        crop_2_y1 = "0"
    dict_return["crop_2_y1"] = crop_2_y1

    try:
        crop_2_width = config.getint("Crop", "2_width")
    except:
        crop_2_width = "0"
    dict_return["crop_2_width"] = crop_2_width

    try:
        crop_2_height = config.getint("Crop", "2_height")
    except:
        crop_2_height = "0"
    dict_return["crop_2_height"] = crop_2_height

    try:
        crop_3_dx = config.getint("Crop", "3_dx")
    except:
        crop_3_dx = "0"
    dict_return["crop_3_dx"] = crop_3_dx

    try:
        crop_3_dy = config.getint("Crop", "3_dy")
    except:
        crop_3_dy = "0"
    dict_return["crop_3_dy"] = crop_3_dy

    try:
        crop_3_width = config.getint("Crop", "3_width")
    except:
        crop_3_width = "0"
    dict_return["crop_3_width"] = crop_3_width

    try:
        crop_3_height = config.getint("Crop", "3_height")
    except:
        crop_3_height = "0"
    dict_return["crop_3_height"] = crop_3_height

    try:
        crop_gravity = config.getint("Crop", "gravity")
    except:
        crop_gravity = "C"
    dict_return["img_crop_gravity"] = entries.parse_list(
        crop_gravity, ("NW", "N", "NE", "W", "C", "E", "SW", "S", "SE"), "SE"
    )

    return dict_return


def border(file_ini):
    """Border congiguration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        border_on = config.getint("Border", "on")
    except:
        border_on = "0"
    dict_return["img_border_on"] = entries.parse_list(border_on, (0, 1), 0)

    try:
        border_color = config.get("Border", "color")
    except:
        border_color = "#FFFFFF"
    dict_return["img_border_color"] = entries.parse_color(border_color, "#FFFFFF")

    try:
        border_x = config.getint("Border", "size_x")
    except:
        border_x = "10"
    dict_return["img_border_size_x"] = border_x

    try:
        border_y = config.getint("Border", "size_y")
    except:
        border_y = "10"
    dict_return["img_border_size_y"] = border_y

    return dict_return


def vignette(file_ini):
    """Vignette congiguration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        vignette_on = config.getint("Vignette", "on")
    except:
        vignette_on = "0"
    dict_return["on"] = entries.parse_list(vignette_on, (0, 1), 0)

    try:
        color = config.get("Vignette", "color")
    except:
        color = "#FFFFFF"
    dict_return["color"] = entries.parse_color(color, "#FFFFFF")

    try:
        dx = config.getint("Vignette", "dx")
    except:
        dx = "0"
    dict_return["dx"] = dx

    try:
        dy = config.getint("Vignette", "dy")
    except:
        dy = "0"
    dict_return["dy"] = dy

    try:
        radius = config.getint("Vignette", "radius")
    except:
        radius = "0"
    dict_return["radius"] = radius

    try:
        sigma = config.getint("Vignette", "sigma")
    except:
        sigma = "0"
    dict_return["sigma"] = sigma

    return dict_return


def colors(file_ini):
    """Color configuration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        color_on = config.getint("Color", "on")
    except:
        color_on = "0"
    dict_return["color_on"] = entries.parse_list(color_on, (0, 1), 0)

    try:
        black_white = config.getint("Color", "black-white")
    except:
        black_white = "1"
    dict_return["black_white"] = entries.parse_list(black_white, (1, 2), 1)

    try:
        bw_sepia = config.getint("Color", "sepia")
    except:
        bw_sepia = "95"
    dict_return["sepia"] = bw_sepia

    return dict_return


def normalize(file_ini, channels):
    """Normalize"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        normalize_on = config.getint("Normalize", "on")
    except:
        normalize_on = 0
    dict_return["normalize_on"] = entries.parse_list(normalize_on, (0, 1), 0)

    try:
        normalize_variant = config.getint("Normalize", "normalize")
    except:
        normalize_variant = 1
    dict_return["normalize"] = entries.parse_list(normalize_variant, (1, 2), 1)

    try:
        normalize_type = config.get("Normalize", "channel")
    except:
        normalize_type = "None"
    dict_return["channel"] = entries.parse_list(normalize_type, channels, "None")

    return dict_return


def contrast(file_ini, contrast_selection_valid_list):
    """Contrast configuration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        contrast_on = config.getint("Contrast", "on")
    except:
        contrast_on = "0"
    dict_return["contrast_on"] = entries.parse_list(contrast_on, (0, 1), 0)

    try:
        contrast_variant = config.getint("Contrast", "contrast")
    except:
        contrast_variant = "1"
    dict_return["contrast"] = entries.parse_list(contrast_variant, (1, 2, 3), 1)

    try:
        contrast_selection = config.get("Contrast", "selection")
    except:
        contrast_selection = "0"
    dict_return["contrast_selection"] = entries.parse_list(
        contrast_selection, contrast_selection_valid_list, "+1"
    )

    try:
        contrast_stretch_1 = float(config.get("Contrast", "stretch1"))
    except:
        contrast_stretch_1 = "0.15"
    dict_return["contrast_stretch_1"] = contrast_stretch_1

    try:
        contrast_stretch_2 = float(config.get("Contrast", "stretch2"))
    except:
        contrast_stretch_2 = "0.05"
    dict_return["contrast_stretch_2"] = contrast_stretch_2

    return dict_return


def logo(file_ini):
    """Logo cofiguration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        logo_on = config.getint("Logo", "on")
    except:
        logo_on = 0
    dict_return["img_logo_on"] = entries.parse_list(logo_on, (0, 1), 0)

    try:
        logo_filename = config.get("Logo", "logo")
    except:
        logo_filename = ""
    dict_return["logo_logo"] = logo_filename

    try:
        logo_gravity = config.get("Logo", "gravity")
    except:
        logo_gravity = "SE"
    dict_return["img_logo_gravity"] = entries.parse_list(
        logo_gravity, ("NW", "N", "NE", "W", "C", "E", "SW", "S", "SE"), "SE"
    )

    try:
        logo_width = config.getint("Logo", "width")
    except:
        logo_width = "100"
    dict_return["logo_width"] = logo_width

    try:
        logo_height = config.getint("Logo", "height")
    except:
        logo_height = "100"
    dict_return["logo_height"] = logo_height

    try:
        logo_dx = config.getint("Logo", "dx")
    except:
        logo_dx = "5"
    dict_return["logo_dx"] = logo_dx

    try:
        logo_dy = config.getint("Logo", "dy")
    except:
        logo_dy = "5"
    dict_return["logo_dy"] = logo_dy

    return dict_return


def mirror(file_ini):
    """Rotate configuration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        mirror_on = config.getint("Mirror", "on")
    except:
        mirror_on = "0"
    dict_return["img_mirror_on"] = entries.parse_list(mirror_on, (0, 1), 0)

    try:
        flip = config.getint("Mirror", "flip")
    except:
        flip = "0"
    dict_return["img_mirror_flip"] = entries.parse_list(flip, (0, 1), 0)

    try:
        flop = config.getint("Mirror", "flop")
    except:
        flop = "0"
    dict_return["img_mirror_flop"] = entries.parse_list(flop, (0, 1), 0)

    return dict_return


def compose(file_ini, preview_size_list):
    """Compose congiguration"""

    # output dictionary
    dict_return = {}

    config = configparser.ConfigParser()
    config.read(file_ini, encoding="utf8")

    try:
        on = config.getint("Compose", "on")
    except:
        on = "0"
    dict_return["compose_on"] = entries.parse_list(on, (0, 1), 0)

    try:
        file = config.get("Compose", "filename")
    except:
        file = ""
    dict_return["compose_filename"] = file

    try:
        right = config.getint("Compose", "right")
    except:
        right = 0
    dict_return["compose_right"] = entries.parse_list(right, (0, 1), 0)

    try:
        autoresize = config.getint("Compose", "autoresize")
    except:
        autoresize = 1
    dict_return["compose_autoresize"] = entries.parse_list(autoresize, (0, 1), 1)

    try:
        color = config.get("Compose", "color")
    except:
        color = "#FFFFFF"
    dict_return["compose_color"] = entries.parse_color(color, "#FFFFFF")

    try:
        gravity = config.get("Compose", "gravity")
    except:
        gravity = "C"
    dict_return["compose_gravity"] = entries.parse_list(
        gravity, ("N", "W", "C", "E", "S"), "C"
    )

    try:
        preview = config.getint("Compose", "preview")
    except:
        preview = 400
    dict_return["preview"] = entries.parse_list(preview, preview_size_list, 400)
    return dict_return


# EOF
