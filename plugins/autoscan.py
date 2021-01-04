#!/usr/bin/python3
#-*- coding: utf-8 -*-
import os
import json
import sys
import socket
import re

#PATH
path = os.getcwd()
cache = (path+'/cache')
plugins = (path + '/plugins')

#GET TARGET
f = open(cache+'/url.cache')
target = f.read()
print("\033[1;33m [+] Target: \033[0m" ,target)

#Survival test, domain name is converted to IP
print("\033[1;33m [+] Check if the target is alive...\n \033[0m")
print("\033[1;33m [+] Get IP address..\n \033[0m")
print ( " [+] " , socket.gethostbyname(target))
ip = socket.gethostbyname(target)
with open(cache + '/ip.cache', 'w') as f:
    f.write(ip)





#IP address location
print("\033[1;33m [+] IP location: \033[0m")

##API

country = os.popen("curl -s http://ip-api.com/line/%s?fields=country"% (target) ) .read()
city = os.popen("curl -s http://ip-api.com/line/%s?fields=city"%(target)).read()
isp = os.popen("curl -s http://ip-api.com/line/%s?fields=isp"%(target)).read()
print("\033[1;34m [+] Country: %s\033[0m" %(country))
print("\033[1;34m [+] City: %s\033[0m" %(city))
print("\033[1;34m [+] ISP: %s\033[0m" %(isp))


#CMS Scan
print("\033[1;33m [+] CMS: \033[0m")
try:
    cms_tmp = os.popen('curl -s -G https://whatcms.org/API/CMS \
    --data-urlencode key="5926b162fde6d3da25520ef5dc0512f8556e637009b72aed3b7576c527766c487a3510" \
    --data-urlencode url="%s"'%(target)).read()
    cms = json.loads(cms_tmp)
    print(" [+]",cms['result']['name'])
except (RuntimeError, TypeError, NameError,ConnectionRefusedError,UnboundLocalError,KeyboardInterrupt):
    print(" [+] Error,Ignore CMS Scan.")

#port scan
print("\033[1;33m [+] Port Scan: \033[0m")

try:
    os.system("python3 %s/portscan_module.py | tee %s/tmp_port.cache "%(plugins,cache))
    #Extract valid information
    lineList = []
    matchPattern = re.compile(r'closed')
    file = open(cache+'/tmp_port.cache','r')
    while 1:
        line = file.readline()
        if not line:
            pass
            break
        elif matchPattern.search(line):
            pass
        else:
            lineList.append(line)
    file.close()
    file = open(cache+'/port.cache', 'w')
    for i in lineList:
        file.write(i)
    file.close()

    print(" [+] Wait...")
except (RuntimeError, TypeError, NameError,ConnectionRefusedError,UnboundLocalError,KeyboardInterrupt):
    print(" [+] Error,Ignore Port Scan.")


#path scan
print("\033[1;33m [+] Path Scan: \033[0m")
try:
    os.system("python3 %s/dirscan_module.py"%plugins)
except (RuntimeError, TypeError, NameError,ConnectionRefusedError,UnboundLocalError,KeyboardInterrupt):
    print(" [+] Error,Ignore Path Scan.")

#service scan
print("\033[1;33m [+] Service Scan: \033[0m")

#Vulnerability scan
print("\033[1;33m [+] Vulnerability Scan: \033[0m")

#Delete cache
