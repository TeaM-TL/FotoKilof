# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" call ImageMagick command """

import os
import platform
import shutil
import sys

import common

def pre_imagick(file_in, destination):
    """
    file_in - original file for processing
    destination - processing directory
    file_out - fullname file for processing in destination
    """

    # Zakładanie katalogu na obrazki wynikowe - podkatalog folderu z obrazkiem
    out_dir = os.path.join(os.path.dirname(file_in), destination)
    if file_in is not None:
        if os.path.isdir(out_dir) is False:
            try:
                os.mkdir(out_dir)
            except:
                print("! Error in pre_imagick: Nie można utworzyć katalogu na przemielone rysunki")
                return None
    else:
        return None

    # Kopiowanie oryginału do miejsca mielenia
    file_out = os.path.join(out_dir, os.path.basename(file_in))
    if file_out is not None:
        try:
            shutil.copyfile(file_in, file_out)
        except IOError as error:
            print("! Error in pre_imagick: Unable to copy file. %s" % error)
            exit(1)
        except:
            print("! Error in pre_imagick: Unexpected error:", sys.exc_info())
            exit(1)
    else:
        file_out = None
        print("! pre_imagemagic: No selected file")
    return file_out


def imagick(cmd, file_out, command):
    """
    run imagemagick command.
    cmd - command for imagemagick
    file_out - fullname picture for processing
    command: convert, mogrify, composite - imagemagick tools
    """
    if cmd != "":
        if file_out is not None:
            if os.path.isfile(file_out):
                file_out = common.spacja(file_out)
                if platform.system() == "Windows":
                    suffix = ".exe "
                else:
                    suffix = " "
                command = command + suffix + cmd + " " + file_out
                print(command)
                try:
                    os.system(command)
                except:
                    print("! Error in imagick: " + command)
                    result = "None"
                else:
                    result = "OK"
            else:
                print("No file for processing")
        else:
            print("No file for imagick")
            result = "None"
    else:
        result = "None"
    return result

# EOF
