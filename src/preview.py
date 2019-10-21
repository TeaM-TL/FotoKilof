# -*- coding: utf-8 -*-

""" moduł z funkcjami ogólnego przeznaczenia """

import os
from PIL import Image

import common
import magick

def preview_histogram(file, dir_temp, gm_or_im):
    """
    histogram generation
    file - fullname image file
    dir_temp - fullname temporary directory
    --
    return: fullname of histogram
    """

    file_histogram = common.spacja(os.path.join(dir_temp, "histogram.png"))
    file = common.spacja(file)

    command = magick.magick_command(gm_or_im + "convert") + file \
        + " -colorspace Gray -define histogram:unique-colors=false histogram:" \
        + file_histogram
    print(command)
    try:
        os.system(command)
        return file_histogram
    except:
        print("! Error in convert_histogram: " + command)


def preview_convert(file, dir_temp, command, size, gm_or_im):
    """
    preview generation
    file - fullname image file
    dir_temp - fullname temporary directory
    command - additional command for imagemagick or space
    --
    return: fullname preview file and size
    """

    img = Image.open(file)
    width = str(img.size[0])
    height = str(img.size[1])

    file_preview = common.spacja(os.path.join(dir_temp, "preview.ppm"))
    command = magick.magick_command(gm_or_im + "convert") \
        + common.spacja(file) \
        + " -resize " + str(size) + "x" + str(size) \
        + command + file_preview
    # print("!", command)
    try:
        os.system(command)
    except:
        print("! Error in preview_convert: " + command)

    try:
        return {'filename': file_preview, 'width': width, 'height': height}
    except:
        print("! Error in preview_convert: return")
        return None

# EOF
