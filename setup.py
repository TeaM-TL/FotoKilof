# -*- coding: utf-8 -*-
""" setup """
from setuptools import setup, find_packages
from fotokilof import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=version.__appname__,
    version=version.__version__,
    author=version.__author__,
    author_email=version.__email__,
    description=version.__description__,
    keywords=version.__keywords__,
    url=version.__url__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "FindSystemFontsFilename",
        "pillow",
        "requests",
        "ttkbootstrap",
        "wand",
        "pywin32; platform_system=='Windows'",
        "pyperclipimg",
    ],
    entry_points={
        "gui_scripts": [
            "fotokilof = fotokilof:__main__",
        ]
    },
)
