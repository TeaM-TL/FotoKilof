# -*- coding: utf-8 -*-
"""
Copyright (c) 2019-2023 Tomasz Łuczak, TeaM-TL

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

function for GUI:
- copy_to_clipboard - copy result into clipboard (only Windows)
- only_numbers - validate only natural values
- only_integer - validate integer values
"""

from io import BytesIO
import logging
import platform
import re
from PIL import Image

import common

if platform.system() == "Windows":
    import win32clipboard
elif platform.system() == "Darwin":
    import subprocess


module_logger = logging.getLogger(__name__)


def copy_to_clipboard(file_in, operating_system):
    """
    Copy results into clipboard for Windows
    https://stackoverflow.com/questions/34322132/copy-image-to-clipboard
    Copy results into clipboard for Macos
    https://stackoverflow.com/questions/54008175/copy-an-image-to-macos-clipboard-using-python?rq=4
    debug needed!
    """
    if operating_system == "Windows":
        # Create an in-memory file-like object
        image_buffer = BytesIO()
        image = Image.open(common.spacja(file_in, operating_system))
        image.convert("RGB").save(image_buffer, "BMP")
        data = image_buffer.getvalue()[14:]

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        image_buffer.close()
    elif operating_system == "MACOS":
        try:
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    'set the clipboard to (read (POSIX file "'
                    + file_in
                    + '") as JPEG picture)',
                ]
            )
            module_logger.debug(
                "Successful copied result into clipboard under MacOS: %s", file_in
            )
        except:
            module_logger.debug(
                "Failed copied result into clipboard under MacOS: %s", file_in
            )


def only_numbers(char):
    """Validation entry widgets: only digits"""
    return char.isdigit()


def only_integer(char):
    """Validation entry widgets: only digits"""
    if re.match("^[-]{0,1}[0-9]{,6}$", str(char)):
        result = True
    else:
        result = False
    return result


# EOF
