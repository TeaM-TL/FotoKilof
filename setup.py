import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FotoKilof",
    version="3.2.2",
    author="Tomasz Luczak",
    author_email="tlu@team-tl.pl",
    description="Nice gui for ImageMagick",
    keywords='GUI ImageMagick',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TeaM-TL/FotoKilof",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_require = ["mo_installer"],
    locale_src = "src/locale",
#    packages_dir={'': 'src'},
#    package_data={'fotokilof': ['src/locale//LC_MESSAGES/.mo']},
    install_requires=['configparser','datetime','pathlib','tkcolorpicker']
#    scripts=['bin/fotokilof']
)
