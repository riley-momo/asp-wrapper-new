#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from distutils.core import setup

__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2018 Patrick Hohenecker\n"
        "\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n"
        "\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n"
        "\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE."
)
__license__ = "MIT License"
__version__ = "2018.1"
__date__ = "May 09, 2018"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


# read the long description from the read me file
long_description = open("README.md").read()

setup(
        author="Patrick Hohenecker",
        author_email="mail@paho.at",
        classifiers=[
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3"
        ],
        copyright="Copyright (c) 2018 Patrick Hohenecker",
        data_files=[
                (".", ["LICENSE", "README.md"])
        ],
        description="A wrapper for accessing ASP solvers from Python.",
        download_url="https://github.com/phohenecker/asp-wrapper/archive/v2018.1.tar.gz",
        install_requires=[],
        license="MIT License",
        long_description=long_description,
        name="aspwrapper",
        package_dir={"": "src/main/python"},
        packages=["aspwrapper"],
        python_requires=">=3",
        url="https://github.com/phohenecker/asp-wrapper",
        version="2018.1"
)
