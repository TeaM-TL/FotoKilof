# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" call ImageMagick command """

import os
import re
import shutil
import tempfile
import touch

import common
import mswindows


def pre_magick(file_in, destination, extension):
    """
    file_in - original file for processing
    destination - output directory
    extension - extension of result file, for change format (jpg->png)
    file_out - fullname file for processing in destination
    """
    result = "OK"  # initial value
    if file_in is not None:
        if os.path.isfile(file_in):
            # making output diretory if not exist
            out_dir = os.path.join(os.path.dirname(file_in), destination)
            if os.path.isdir(out_dir) is False:
                try:
                    os.mkdir(out_dir)
                except:
                    print("! Error in pre_imagick: Nie można utworzyć katalogu na przemielone rysunki")
                    result = None
        else:
            result = None
    else:
        result = None

    if result == "OK":
        # preparing output filename
        file_in_without_ext = os.path.splitext(file_in)
        file_out = os.path.join(out_dir, os.path.basename(file_in_without_ext[0] + extension))
    else:
        file_out = None
    return file_out


def magick(cmd, file_in, file_out, command):
    """
    run imagemagick command.
    cmd - command for imagemagick
    file_in - fullname picture for processing
    file_out - fullname output picture
    command: it depends:
      convert, mogrify, composite - ImageMagick
      gm convert, gm mogrify, gm composite - GraphicsMagick
    """
    result = None
    if cmd != "":
        if file_in is not None:
#            if os.path.isfile(file_in):
            file_in = common.spacja(file_in)
            file_out = common.spacja(file_out)
            command = magick_command(command)
            command = command + " " + file_in  + " " + cmd + file_out
            # print("Execute: ", command)
            try:
                os.system(command)
            except:
                print("! Error in imagick: " + command)
                result = None
            else:
                result = "OK"
        else:
            print("imagick: No file for imagick")
            result = None
    else:
        result = None
    return result


def magick_command(command):
    """
    make [Graphics|Image]Magick independent
    command: it depends:
    - ImageMagick:
      - Unix: convert, mogrify, composite
      - Windows: magick.exe convert, magick.exe mogrify, magick.exe composite
    - GraphicsMagick:
      - Unix: gm convert, gm mogrify, gm composite
      - Windows: gm.exe convert, gm.exe mogrify, gm.exe composite
    """
    if mswindows.windows() == 1:
        suffix = ".exe "
    else:
        suffix = " "
    tool = command.split()
    tool.insert(1, suffix)
    tool.extend(' ')
    result = "".join(tool)
    return result


def fonts_list_get(gm_or_im):
    """ get available font list from imagemagick """

    fonts_list = None
    file_font = os.path.join(tempfile.gettempdir(), "fonts_list")
    command = " -list font > "
    result = magick(command, "", file_font, gm_or_im + "convert")
    if result is not None:
        try:
            file = open(file_font, "r")
        except:
            print("!fonts_list_get: cannot read file_font")
        else:
            fonts_list = []
            if gm_or_im == "gm ":
                # GraphicsMagick format
                for line in file:
                    if re.search("\\d$", line) is not None:
                        line = re.findall('^[-a-zA-Z]+', line)
                        fonts_list.append(line)
            else:
                # ImageMagick format
                for line in file:
                    if re.search("Font", line) is not None:
                        line = re.sub('^[ ]+Font:[ ]*', "", line)
                        line = re.sub('\n', "", line)
                        fonts_list.append(line)
            file.close()
            try:
                os.remove(file_font)
            except:
                print("!fonts_list_get: cannot remove file_font")

    if fonts_list is None or len(fonts_list) == 0:
        fonts_list = ["Helvetica"]
    return fonts_list


def get_magick_version(gm_or_im):
    """ get version of *Magick """

    version = ""
    if gm_or_im == None:
        gm_or_im = ""

    file_version = common.spacja(os.path.join(tempfile.gettempdir(),
                                              "version"))
    touch.touch(file_version)
    command = "-Version > "
    result = magick(command, "", common.spacja(file_version),
                    gm_or_im + "convert")
    if result is not None:
        try:
            file = open(file_version, "r")
        except:
            print("!get_magick_version: cannot read file_version")
        else:
            version_object = re.search("\\d+[.]\\d+([.]\\d+)*", file.readline())
            if version_object is not None:
                version = version_object[0]
            file.close()
            try:
                os.remove(file_version)
            except:
                print("!get_magick_version: cannot remove file_version")

    return version


def check_magick():
    """
    What is available: ImageMagick, Graphick Magick or none
    """
    if mswindows.windows() == 1:
        suffix = ".exe"
    else:
        suffix = ""
    if check_imagemagick(suffix) is not None:
        version = "IM"
        if mswindows.windows() == 1:
            result = "magick "
        else:
            result = ""
    elif check_graphicsmagick(suffix) is not None:
        version = "GM"
        result = "gm "
    else:
        version = ""
        result = None

    return (result, version)


def check_imagemagick(suffix):
    """ Check if ImageMmagick is avaialble"""
    if shutil.which('convert' + suffix):
        result1 = "OK"
    else:
        result1 = None

    if shutil.which('mogrify' + suffix):
        result2 = "OK"
    else:
        result2 = None

    if shutil.which('compose' + suffix):
        result3 = "OK"
    else:
        result3 = None

    if shutil.which('identify' + suffix):
        result4 = "OK"
    else:
        result4 = None

    if result1 is not None and result2 is not None and result3 is not None and result4 is not None:
        result = "OK"
    else:
        result = None

    return result


def check_graphicsmagick(suffix):
    """ Check if GraphicsMagick is avaialble"""
    if shutil.which('gm' + suffix):
        result = "OK"
    else:
        result = None

    return result


def get_image_size(file_in, gm_or_im):
    """
    identify width and height of picture
    input: file name
    output: width and height
    """

    width = 1
    height = 1
    size = ""
    profiles = ""
    bit_depth = ""
    colors = ""
    colorspace = ""
    compression = ""
    basename = ""
    file_info = common.spacja(os.path.join(tempfile.gettempdir(), "image_info"))
    touch.touch(file_info)
    # without n%[profiles] - not available in IM < 7.0
    command = ' -format "%[width]\\n%[height]\\n%[size]\\n%[bit-depth]\\n%[colors]\\n%[colorspace]\\n%[compression]\\n%[basename]" '
    command = command + common.spacja(file_in) + ' > '
    result = magick(command, "", file_info, gm_or_im + "identify")
    if result is not None:
        try:
            file = open(file_info, "r")
        except:
            print("!get_image_size: cannot read file_info")
        else:
            width = int(file.readline())
            height = int(file.readline())
            size = file.readline()
            bit_depth = file.readline()
            colors = file.readline()
            colorspace = file.readline()
            compression = file.readline()
            basename = file.readline()
            # profiles = file.readline()
            file.close()
            try:
                os.remove(file_info)
            except:
                print("!get_image_size: cannot remove file_info")
    print("identify: ", basename, "\n", width, "x", height, "\n", size, "\n",
          profiles, bit_depth, colors, colorspace, compression)
    return (width, height, size)


def display_image(file_in, gm_or_im):
    """ display image """
    file_in = common.spacja(file_in)
    if mswindows.windows() == 1:
        display = "IMDisplay"
        ampersand = ''
    else:
        display = "display"
        ampersand = ' &'

    command = magick_command(gm_or_im + display)
    command = command + " " + file_in + ampersand
    # print("Execute: ", command)
    try:
        os.system(command)
    except:
        print("! Error in imagick: " + command)
        result = None
    else:
        result = "OK"

    return result

# EOF
