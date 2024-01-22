#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from datetime import datetime

base_url = "https://archive.topshelfaquatics.com/output"
file_name = f"{base_url}/test_time_file.txt"
# file_name = "time_file.txt"

if not os.path.exists(file_name):
    open(file_name, mode='w').close()

with open(file_name, mode='a+') as f:
    f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    f.write("\n")
