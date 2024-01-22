#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from datetime import datetime

from dotenv import dotenv_values

from .static_data import PRODUCTS_FILE_DIR


def get_output_file_dir():
    # config = dotenv_values(".env")
    # return config['PRODUCTS_FILE_DIR'].rstrip('/')
    return PRODUCTS_FILE_DIR.rstrip('/')


file_name = f"{get_output_file_dir()}/test_time_file.txt"
# file_name = "time_file.txt"

if not os.path.exists(file_name):
    open(file_name, mode='w').close()

with open(file_name, mode='a+') as f:
    f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    f.write("\n")
