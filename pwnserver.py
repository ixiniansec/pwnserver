#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
import sys
import pyfiglet



ascii_banner = pyfiglet.figlet_format("PwnServer")
print(ascii_banner)


from lib.utils import check
from lib.utils import start
