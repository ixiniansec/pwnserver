#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os


#ROOT CHECK
if os.geteuid() != 0:
    print("\033[1;31m This program must be run as root. Aborting. \033[0m")
    exit()





