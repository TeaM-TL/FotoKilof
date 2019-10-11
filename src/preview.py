# -*- coding: utf-8 -*-

""" moduł z funkcjami ogólnego przeznaczenia """

import os
import platform
from PIL import Image
import common


def preview_histogram(file, dir_temp):
    """
    histogram generation
    file - fullname image file
    dir_temp - fullname temporary directory
    --
    return: fullname of histogram
    """

    file_histogram = common.spacja(os.path.join(dir_temp, "histogram.png"))
    file = common.spacja(file)

    if platform.system() == "Windows":
        suffix = ".exe "
    else:
        suffix = " "
    command = "convert" + suffix + file \
        + " -colorspace Gray -define histogram:unique-colors=false histogram:" \
        + file_histogram
    try:
        os.system(command)
        return file_histogram
    except:
        print("! Error in convert_histogram: " + command)


def preview_convert(file, dir_temp, command, size):
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

    file_preview = os.path.join(dir_temp, "preview.ppm")
    file = common.spacja(file)
    file_preview = common.spacja(file_preview)

    if platform.system() == "Windows":
        suffix = ".exe "
    else:
        suffix = " "
    command = "convert" + suffix + file + \
        " -resize " + str(size) + "x" + str(size) \
        + command + file_preview
    # print(command)
    try:
        os.system(command)
    except:
        print("! Error in convert_preview: " + command)

    try:
        return {'filename': file_preview, 'width': width, 'height': height}
    except:
        print("! Error in convert_preview: return")
        return None

# EOF
