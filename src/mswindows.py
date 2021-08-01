# -*- coding: utf-8 -*-

"""
Copyright (c) 2019-2020 Tomasz Łuczak, TeaM-TL

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
"""

""" Windows specific module """

import io
import ctypes
from PIL import Image
import platform

def windows():
    """ checking: system Windows or normal OS """
    if platform.system() == "Windows":
        result = 1
    else:
        result = 0
    return result


def windows_copy_to_clipboard(file_in):
    """
    https://stackoverflow.com/questions/21319486/copy-pil-pillow-image-to-windows-clipboard
    """

    msvcrt = ctypes.cdll.msvcrt
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32


    img = Image.open(file_in)
    output = io.BytesIO()
    img.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    CF_DIB = 8
    GMEM_MOVEABLE = 0x0002

    global_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
    global_data = kernel32.GlobalLock(global_mem)
    msvcrt.memcpy(ctypes.c_char_p(global_data), data, len(data))
    kernel32.GlobalUnlock(global_mem)
    user32.OpenClipboard(None)
    user32.EmptyClipboard()
    user32.SetClipboardData(CF_DIB, global_mem)
    user32.CloseClipboard()


# EOF
