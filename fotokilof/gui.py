# -*- coding: utf-8 -*-
"""
Copyright (c) 2019-2025 Tomasz Łuczak, TeaM-TL

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

if platform.system() != "Windows":
    import subprocess

if platform.system() in ("Linux", "Darwin", "Windows"):
    import pyperclipimg
    USE_PYPERCLIP = 1
else:
    USE_PYPERCLIP = 0

module_logger = logging.getLogger(__name__)


def copy_to_clipboard(file_in):
    """
    Copy results into clipboard for Windows
    https://stackoverflow.com/questions/34322132/copy-image-to-clipboard
    Copy results into clipboard for Macos
    https://stackoverflow.com/questions/54008175/copy-an-image-to-macos-clipboard-using-python?rq=4
    debug needed!
    """
    if USE_PYPERCLIP:
        pyperclipimg.copy(file_in)
    else:
        # e.g. FreeBSD
        with Image.open(file_in) as image:
            image_buffer = BytesIO()
            image.save(image_buffer, format="png")
            try:
                output = subprocess.Popen(
                    ("xclip", "-selection", "clipboard", "-t", "image/png", "-i"),
                    stdin=subprocess.PIPE,
                )
                # write image to stdin
                output.stdin.write(image_buffer.getvalue())
                output.stdin.close()
            except:
                module_logger.debug(
                    "Failed copied result into clipboard under Unix: %s. Did you install xclip?",
                    file_in,
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
