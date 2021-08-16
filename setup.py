import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pkg_vars = {}
with open("src/version.py") as fp:
    exec(fp.read(), pkg_vars)
setuptools.setup(
    name=pkg_vars['__appname__'],
    version=pkg_vars['__version__'],
    author=pkg_vars['__author__'],
    author_email=pkg_vars['__email__'],
    description=pkg_vars['__description__'],
    keywords=pkg_vars['__keywords__'],
    url=pkg_vars['__url__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pillow','tkcolorpicker'],
    entry_points = {
        "gui_scripts": [
            "fotokilof = src:__main__",
        ]
    },
    include_package_data=True,
)

