#!/usr/bin/env bash

# MIT License
#
# Copyright (c) 2018 Patrick Hohenecker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# author:   Patrick Hohenecker <mail@paho.at>
# version:  2018.1
# date:     May 09, 2018


# check if a path to a DLV executable has been provided
if [ ${#} != 1 ]; then
    echo "usage: run-tests.sh [PATH_TO_DLV]"
    exit 1
fi

# add symbolic link to DLV to the resources directory
DLV_LINK="`pwd`/src/test/resources/test-dlv.bin"
ln -s "${1}" "${DLV_LINK}"

# run unit tests
export PATH="`pwd`/src/test/resources:${PATH}"
export PYTHONPATH="`pwd`/src/main/python:${PYTHONPATH}"
python3 -m unittest discover -s src/test/python -p "*_test.py"

# remove the previously created link to DLV
rm "${DLV_LINK}"
