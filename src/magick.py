# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
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

module to work with *Magick:
- pre_magick - prepare output file for conversion
- magick - picture conversion
- magick_command - make [Graphics|Image]Magick independent
- display_image - display picture
- get_image_size - identify picture: width and height
- get_fonts_dict - get available fonts dict
- get_magick_version - get version of *Magick
- check_magick - check what is available
- check_imagemagick - checker for ImageMagick
- check_graphickmagick - checker for GraphicsMagick
"""

import os
import re
import shutil
import tempfile

import common
import log
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
                    log.write_log("pre_imagick: Cannot make directory for output pictures", "E")
                    result = None
        else:
            result = None
    else:
        result = None

    if result == "OK":
        # preparing output filename
        file_in_without_ext = os.path.splitext(file_in)
        file_out = os.path.join(out_dir,
                                os.path.basename(file_in_without_ext[0] \
                                                 + extension))
    else:
        file_out = None
    return file_out


def magick(cmd, file_in, file_out, command):
    """
    run imagemagick command.
    cmd - command for imagemagick
    file_in - fullname picture for processing
    file_out - fullname output picture
    command:
      convert, mogrify, composite, import - ImageMagick
      gm convert, gm mogrify, gm composite, gm import - GraphicsMagick
    """
    result = None
    if cmd != "":
        if file_in is not None:
            file_in = common.spacja(file_in)
            file_out = common.spacja(file_out)
            command = magick_command(command)
            command = command + " " + file_in  + " " + cmd + file_out
            log.write_log("Execute: " + command, "M")
            try:
                os.system(command)
            except:
                log.write_log("Errot in imagick: " + command, "E")
                result = None
            else:
                result = "OK"
        else:
            log.write_log("imagick: No file for imagick", "W")
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


def get_fonts_dict(gm_or_im):
    """ get available font dict (name: path) from imagemagick """

    fonts_list = None
    file_font = os.path.join(tempfile.gettempdir(),
                             "fotokilof_" + os.getlogin() + "_fonts_list")
    command = " -list font > "
    result = magick(command, "", file_font, gm_or_im + "convert")
    if result is not None:
        try:
            file = open(file_font, "r")
        except:
            log.write_log("get_fonts_list: cannot read file_font", "E")
        else:
            fonts_name = []
            fonts_path = []
            if gm_or_im == "gm ":
                # GraphicsMagick format
                for line in file:
                    if re.search("\\d$", line) is not None:
                        line = re.findall('^[-a-zA-Z]+', line)
                        fonts_dict[line] = ""
            else:
                # ImageMagick format
                for line in file:
                    if re.search("^[ ]+Font:", line) is not None:
                        line = re.sub('^[ ]+Font:[ ]*', "", line)
                        line = re.sub('\n', "", line)
                        fonts_name.append(line)
                    elif re.search("^[ ]+glyphs:", line) is not None:
                        line = re.sub('^[ ]+glyphs:[ ]*', "", line)
                        line = re.sub('\n', "", line)
                        fonts_path.append(line)

                # conversion two list into dictionary
                fonts_dict = dict(zip(fonts_name, fonts_path))
            file.close()
            try:
                os.remove(file_font)
            except:
                log.write_log("get_fonts_list: cannot remove file_font", "W")

    if fonts_dict is None or len(fonts_dict) == 0:
        fonts_dict["Helvetica"] = ""

    return fonts_dict


def get_magick_version(gm_or_im):
    """ get version of *Magick """

    version = ""
    if gm_or_im is None:
        gm_or_im = ""

    file_version = common.spacja(os.path.join(tempfile.gettempdir(),
                                              "fotokilof_" + \
                                              os.getlogin() + "_version"))

    command = "-Version > "
    result = magick(command, "", common.spacja(file_version),
                    gm_or_im + "convert")
    if result is not None:
        try:
            file = open(file_version, "r")
        except:
            log.write_log("get_magick_version: cannot read file_version", "W")
        else:
            version_object = re.search("\\d+[.]\\d+([.]\\d+)*", file.readline())
            if version_object is not None:
                version = version_object[0]
            file.close()
            try:
                os.remove(file_version)
            except:
                log.write_log("get_magick_version: cannot remove file_version", "W")

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
    """ Check if ImageMagick is avaialble"""

    if mswindows.windows() == 1:
        if shutil.which('magick' + suffix):
            result = "OK"
        else:
            result = None
    else:
        if shutil.which('convert'):
            result = "OK"
            if shutil.which('mogrify'):
                result = "OK"
                if shutil.which('composite'):
                    result = "OK"
                    if shutil.which('identify'):
                        result = "OK"
                    else:
                        result = None
                else:
                    result = None
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
    file_info = common.spacja(os.path.join(tempfile.gettempdir(),
                                           "fotokilof_" + os.getlogin() \
                                           + "_image_info"))

    command = ' -format "%w\\n%h\\n%b" '
    command = command + common.spacja(file_in) + ' > '
    result = magick(command, "", file_info, gm_or_im + "identify")
    if result is not None:
        try:
            file = open(file_info, "r")
        except:
            log.write_log("get_image_size: cannot read file_info", "W")
        else:
            width = int(file.readline())
            height = int(file.readline())
            size = file.readline()
            file.close()
            try:
                os.remove(file_info)
            except:
                log.write_log("get_image_size: cannot remove image_info", "W")
    return (width, height, size)


def display_image(file_in, gm_or_im):
    """ display image """
    file_in = common.spacja(file_in)
    if mswindows.windows() == 1:
        display = 'explorer'  # this is the best idea for Windows
        ampersand = ''
    else:
        display = gm_or_im + "display"
        ampersand = ' &'

    command = magick_command(display)
    command = command + " " + file_in + ampersand
    log.write_log("Execute: " + command, "M")
    try:
        os.system(command)
    except:
        log.write_log(" Error in imagick: " + command, "E")
        result = None
    else:
        result = "OK"

    return result

# EOF
