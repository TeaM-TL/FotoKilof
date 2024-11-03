# -*- coding: utf-8 -*-
# pylint: disable=bare-except
# pylint: disable=too-many-branches

"""
Copyright (c) 2022-2024 Tomasz Łuczak, TeaM-TL

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

module contains function for saving entries from config file.
Every function save part of config file
- cofig - general setting for FotoKilof
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
import logging

import common

module_logger = logging.getLogger(__name__)


def save(ini_data):
    """save values into INI file"""
    # extract data
    file_ini = ini_data[0]
    main = ini_data[1]
    resize = ini_data[2]
    text = ini_data[3]
    rotate = ini_data[4]
    crop = ini_data[5]
    border = ini_data[6]
    color = ini_data[7]
    normalize = ini_data[8]
    contrast = ini_data[9]
    mirror = ini_data[10]
    vignette = ini_data[11]
    logo = ini_data[12]
    compose = ini_data[13]
    # content preparing
    config = configparser.ConfigParser()
    # main
    config.add_section(main["section"])
    config.set(main["section"], "path", main["path"])
    config.set(main["section"], "work_dir", main["work_dir"])
    config.set(main["section"], "file_dir", str(main["file_dir"]))
    config.set(main["section"], "exif", str(main["exif"]))
    config.set(main["section"], "custom", str(main["custom_on"]))
    config.set(main["section"], "preview_orig", main["preview_orig"])
    config.set(main["section"], "preview_new", main["preview_new"])
    config.set(main["section"], "log_level", main["log_level"])
    config.set(main["section"], "check_version", str(main["check_version"]))
    # resize
    config.add_section(resize["section"])
    config.set(resize["section"], "on", str(resize["on"]))
    config.set(resize["section"], "resize", str(resize["resize"]))
    config.set(resize["section"], "size_pixel_x", resize["size_pixel_x"])
    config.set(resize["section"], "size_pixel_y", resize["size_pixel_y"])
    config.set(resize["section"], "size_percent", resize["size_percent"])
    # text
    config.add_section(text["section"])
    config.set(text["section"], "on", str(text["on"]))
    config.set(text["section"], "inout", str(text["inout"]))
    config.set(text["section"], "text", text["text"])
    config.set(text["section"], "gravity", text["gravity"])
    config.set(text["section"], "gravity_onoff", str(text["gravity_onoff"]))
    config.set(text["section"], "font", text["font"])
    config.set(text["section"], "size", text["size"])
    config.set(text["section"], "color", text["color"])
    config.set(text["section"], "box", str(text["box"]))
    config.set(text["section"], "box_color", text["box_color"])
    config.set(text["section"], "x", text["x"])
    config.set(text["section"], "y", text["y"])
    config.set(text["section"], "text_rotate", str(text["text_rotate"]))
    config.set(text["section"], "text_rotate_own", text["text_rotate_own"])
    config.set(text["section"], "text_arrow", str(text["text_arrow"]))
    # rotate
    config.add_section(rotate["section"])
    config.set(rotate["section"], "on", str(rotate["on"]))
    config.set(rotate["section"], "rotate", str(rotate["rotate"]))
    config.set(rotate["section"], "own", rotate["own"])
    config.set(rotate["section"], "color", rotate["color"])
    # crop
    config.add_section(crop["section"])
    config.set(crop["section"], "on", str(crop["on"]))
    config.set(crop["section"], "crop", str(crop["crop"]))
    config.set(crop["section"], "1_x1", crop["1_x1"])
    config.set(crop["section"], "1_y1", crop["1_y1"])
    config.set(crop["section"], "1_x2", crop["1_x2"])
    config.set(crop["section"], "1_y2", crop["1_y2"])
    config.set(crop["section"], "2_x1", crop["2_x1"])
    config.set(crop["section"], "2_y1", crop["2_y1"])
    config.set(crop["section"], "2_width", crop["2_width"])
    config.set(crop["section"], "2_height", crop["2_height"])
    config.set(crop["section"], "3_dx", crop["3_dx"])
    config.set(crop["section"], "3_dy", crop["3_dy"])
    config.set(crop["section"], "3_width", crop["3_width"])
    config.set(crop["section"], "3_height", crop["3_height"])
    config.set(crop["section"], "gravity", crop["gravity"])
    # border
    config.add_section(border["section"])
    config.set(border["section"], "on", str(border["on"]))
    config.set(border["section"], "color", border["color"])
    config.set(border["section"], "size_x", border["size_x"])
    config.set(border["section"], "size_y", border["size_y"])
    # color
    config.add_section(color["section"])
    config.set(color["section"], "on", str(color["on"]))
    config.set(color["section"], "black-white", str(color["black-white"]))
    config.set(color["section"], "sepia", color["sepia"])
    # normalize
    config.add_section(normalize["section"])
    config.set(normalize["section"], "on", str(normalize["on"]))
    config.set(normalize["section"], "normalize", str(normalize["normalize"]))
    config.set(normalize["section"], "channel", normalize["channel"])
    # contrast
    config.add_section(contrast["section"])
    config.set(contrast["section"], "on", str(contrast["on"]))
    config.set(contrast["section"], "contrast", str(contrast["contrast"]))
    config.set(contrast["section"], "selection", contrast["selection"])
    config.set(
        contrast["section"], "contrast_stretch_1", contrast["contrast_stretch_1"]
    )
    config.set(
        contrast["section"], "contrast_stretch_2", contrast["contrast_stretch_2"]
    )
    # mirror
    config.add_section(mirror["section"])
    config.set(mirror["section"], "on", str(mirror["on"]))
    config.set(mirror["section"], "flip", str(mirror["flip"]))
    config.set(mirror["section"], "flop", str(mirror["flop"]))
    # vignette
    config.add_section(vignette["section"])
    config.set(vignette["section"], "on", str(vignette["on"]))
    config.set(vignette["section"], "dx", str(common.empty(vignette["dx"])))
    config.set(vignette["section"], "dy", str(common.empty(vignette["dy"])))
    config.set(vignette["section"], "radius", vignette["radius"])
    config.set(vignette["section"], "sigma", vignette["sigma"])
    config.set(vignette["section"], "color", vignette["color"])
    # logo
    config.add_section(logo["section"])
    config.set(logo["section"], "on", str(logo["on"]))
    config.set(logo["section"], "logo", logo["logo"])
    config.set(logo["section"], "gravity", logo["gravity"])
    config.set(logo["section"], "width", logo["width"])
    config.set(logo["section"], "height", logo["height"])
    config.set(logo["section"], "dx", logo["dx"])
    config.set(logo["section"], "dy", logo["dy"])
    # compose
    config.add_section(compose["section"])
    config.set(compose["section"], "on", str(compose["on"]))
    config.set(compose["section"], "filename", compose["filename"])
    config.set(compose["section"], "right", str(compose["right"]))
    config.set(compose["section"], "autoresize", str(compose["autoresize"]))
    config.set(compose["section"], "color", compose["color"])
    config.set(compose["section"], "gravity", compose["gravity"])
    config.set(compose["section"], "preview", compose["preview"])

    # save to a file
    try:
        with open(file_ini, "w", encoding="utf-8", buffering=1) as configfile:
            config.write(configfile)
    except:
        module_logger.error("ini_save: cannot save config file: %s", file_ini)
