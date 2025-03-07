#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-only
#
# Utility functions to run the unittests
# Copyright (c) 2021 Samsung Electronics Co., Ltd.
#
# @file   test_utils.py
# @brief  Utility functions to run the unittests
# @author Jaeyun Jung <jy1210.jung@samsung.com>
# @date   20 Aug 2021
# @bug    No known bugs

import sys
import os
from itertools import product
from struct import pack


##
# @brief Read file and return its content
def read_file(filename):
    with open(filename, 'rb') as f:
        b = f.read()
    return b


##
# @brief Read labels from file
def read_label(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


##
# @brief Write the data to file
def write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)


##
# @brief Convert given data to bytes
# @param[in] data The data to be converted to bytes array
# @return bytes converted from the data
def convert_to_bytes(data):
    if isinstance(data, bytes):
        return data
    return pack("<B", data)


##
# @brief Compare original content and scaled one
def compare_scaled_tensor(d1, d2, innerdim):
    # data should be tuple (data, width, height)
    data1, width1, height1 = d1
    data2, width2, height2 = d2
    len1 = len(data1)
    len2 = len(data2)

    if (len1 * width2 * height2) != (len2 * width1 * height1):
        print(str(len1 * width2 * height2) + ' / ' + str(len2 * width1 * height1))
        return 1

    if (len1 != width1 * height1 * innerdim) or (len2 != width2 * height2 * innerdim):
        return 2

    for y, x, c in product(range(0, height2), range(0, width2), range(0, innerdim)):
        ix = x * width1 // width2
        iy = y * height1 // height2
        if data1[c + ix * innerdim + iy * width1 * innerdim] != \
                data2[c + x * innerdim + y * width2 * innerdim]:
            print('At ' + str(x) + ',' + str(y))
            return 5

    return 0
