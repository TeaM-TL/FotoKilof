# -*- coding: utf-8 -*-

"""
Copyright (c) 2024 Tomasz Łuczak, TeaM-TL

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

From https://stackoverflow.com/questions/28774852/pypi-api-how-to-get-stable-package-version
"""

import json
import logging
import requests
import time

try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

module_logger = logging.getLogger(__name__)

URL_PATTERN = "https://pypi.org/pypi/{package}/json"


def get_version(url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json."""

    package = "FotoKilof"
    version = parse("0")
    try:
        req = requests.get(url_pattern.format(package=package), timeout=2.50)
        request_success = 1
    except:
        request_success = 0

    if request_success and req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding))
        releases = j.get("releases", [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return (request_success, str(version))


def check_version(current_version):
    """
    Check version of FotoKilof in PyPi
    return 1 - get new
    return 0 - there are no new
    """
    start_time = time.time()
    result = 0
    result_success, result_version = get_version()
    if result_success and result_version > current_version:
        result = 1
    module_logger.info("check_version: %ss", str(time.time() - start_time))
    return (result, result_version)
