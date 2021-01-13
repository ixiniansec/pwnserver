#!/usr/bin/python3
#-*- coding: utf-8 -*-
import os
#Read the open port of the target host
#PATH
path = os.getcwd()
cache = (path+'/cache')

#Filter invalid information
os.popen("cat %s/port.cache | awk '{print $4}' > %s/new_port.cache" %(cache,cache)).read()
os.system("sed ':t;N;s/\\\n/,/;b t' %s/new_port.cache > %s/listen_port.cache"%(cache,cache))

f = open(cache+'/listen_port.cache')
str= f.read()
print(str)