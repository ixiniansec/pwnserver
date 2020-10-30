#!/usr/bin/python3
#-*- coding: utf-8 -*-
import os
import json
import sys 
import socket 


#PATH
path = os.getcwd()
cache = (path+'/cache')
pwn_root_path = (path+'/plugins/pwn_root_path.py')
solrpath = (path+'/scripts/poc/Solr')
weblogicpath = (path+'/scripts/poc/Weblogic')

#GET TARGET
f = open(cache+'/url.cache')
target = f.read()

print("\033[1;33m [+] Target: %s\n \033[0m" %(target))

#IP address location
print("\033[1;33m [+] IP location: \033[0m")

##API

country = os.popen("curl -s http://ip-api.com/line/%s?fields=country"% (target) ) .read()
city = os.popen("curl -s http://ip-api.com/line/%s?fields=city"%(target)).read()
isp = os.popen("curl -s http://ip-api.com/line/%s?fields=isp"%(target)).read()
print("\033[1;34m [+] Country: %s\033[0m" %(country))
print("\033[1;34m [+] City: %s\033[0m" %(city))
print("\033[1;34m [+] ISP: %s\033[0m" %(isp))



#CMS SCAN

print("\033[1;33m [+] CMS: \033[0m")
cms_tmp = os.popen('curl -s -G https://whatcms.org/API/CMS \
--data-urlencode key="5926b162fde6d3da25520ef5dc0512f8556e637009b72aed3b7576c527766c487a3510" \
--data-urlencode url="%s"'%(target)).read()
cms = json.loads(cms_tmp)
print(" [+]",cms['result']['name'])



#PORT SCAN
print("\033[1;33m [+] Port: \033[0m")

try: 
      
    # will scan ports between 1 to 65535 
    for port in range(1,65535): 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        socket.setdefaulttimeout(1) 
          
        # returns an error indicator 
        result = s.connect_ex((target,port)) 
        if result ==0: 
            print(" [+]Port {} is open".format(port)) 
        s.close() 
    
    
except KeyboardIntruppt: 
        print("\n Exitting Program.") 
        pass
except socket.gaierror: 
        print("\n Hostname Could Not Be Resolved.") 
        pass
except socket.error: 
        print("\ Server not responding.") 
        pass


#Path scan
print("\033[1;33m [+] Path Scan: \033[0m")
os.system("python3 %s %s" %(pwn_root_path,target))


#Vulnerability scan Info
print("\033[1;33m [+] Vulnerability scan: \033[0m")
print(" [+] Collecting necessary information, please wait...")
print(" [+] Scanning target service information...")
os.popen("nmap -sS -n -T5 -Pn -p- -sV  %s > %s/nmap.cache " %(target,cache) ) .read()
os.popen("cat %s/nmap.cache | awk '/[0-9]*\/(tcp|udp)/ {print $1$4$5$6}' | sed 's/tcp//g' > %s/version.cache"%(cache,cache))

###Judging the existence of services

def dumper(target_info,servername):
    saving_str = json.dunp(target_info)
    os.mknod("target "+servername+".cache")
    cache_json = open("target "+servername+".cache")
    cache_json.writelines(saving_str)



#SETPATH
version = cache+'/version.cache'
#os.system("cat %s"%(version))

#cache+'/version.cache'
with open(version,'r') as foo:

    for line in foo.readlines():
        
        target_info = {
            "ip":target
        }
      
       
#####JBoss
        if 'JBoss' in line:
            print(" [+] JBoss service exists.")
            target_info['port'] = line.split('/')[0]
            jboss = json.dumps(target_info)
            with open(cache+'/jboss.cache', 'w') as jbossfile:
                jbossfile.write(jboss)

######PostgreSQL
        elif 'PostgreSQL' in line:
            print(" [+] PostgreSQL service exists.")
            target_info['port'] = line.split('/')[0]
            postgresql = json.dumps(target_info)
            with open(cache+'/postgresql.cache', 'w') as postgresqlfile:
                postgresqlfile.write(postgresql)
             
            

#####Tomcat
        elif 'Tomcat' in line:
            print(" [+] Tomcat service exists.")
            target_info['port'] = line.split('/')[0]
            tomcat = json.dumps(target_info)
            with open(cache+'/tomcat.cache', 'w') as tomcatfile:
                tomcatfile.write(tomcat)


#####Weblogic
        elif 'OracleWebLogicadmin' in line:
            print(" [+] Weblogic service exists.")
            target_info['port'] = line.split('/')[0]
            weblogic = json.dumps(target_info)
            with open(cache+'/weblogic.cache', 'w') as weblogicfile:
                weblogicfile.write(weblogic)
            os.system("python3 %s/POC_batch_process.py"%(weblogicpath))

 
 ######Nexus
        elif 'Nexus' in line:
            print(" [+] Nexus service exists.")
            target_info['port'] = line.split('/')[0]
            nexus = json.dumps(target_info)
            with open(cache+'/nexus.cache', 'w') as nexusfile:
                nexusfile.write(nexus)
            

######Solr
        elif 'ApacheSolr' in line:
            print(" [+] Solr service exists.")
            target_info['port'] = line.split('/')[0]
            solr = json.dumps(target_info)
            with open(cache+'/solr.cache', 'w') as solrfile:
                solrfile.write(solr)
            os.system("python3 %s/POC_batch_process.py"%(solrpath))
            

            
        else:
            continue
            print("\033[1;31m [!] The middleware POC is not recorded!\033[0m")
            
            exit()            


