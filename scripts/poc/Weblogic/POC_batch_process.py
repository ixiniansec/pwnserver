import os
import json

#PATH
path = os.getcwd()
syscache = (path+'/cache')
weblogic = (path+'/scripts/poc/Weblogic')
#####DEBUG
#print(cache)

#----------------------------------------------------
#POC_file = open("POC_standard")
#standard_label_file = open("standard_label")
## code above is read two file with POC target information and label information


os.system("cp %s/POC_standard %s/final_execute"%(weblogic,weblogic))


cache = open(path+"/cache/weblogic.cache")



target = json.loads(cache.readline())


key_name = target.keys()

if 'ip' not in key_name:
    target['ip'] = ' '

if 'port' not in key_name:
    target['port'] = ' '

if 'url' not in key_name:
    target['url'] = ' '
    if 'ip' in key_name and 'port' in key_name:
        target['url'] = "http://"+target['ip']+":"+target['port']+"/"

if 'cookies' not in key_name:
    target['cookies'] = ' '

if 'token' not in key_name:
    target['token'] = ' '




#    Standard_executecode = POC_file.readline()
#    Standard_labelname = standard_label_file.readline()
#    if Standard_labelname is 1:
#        Target_code =
#    final_execode_code = Standard_executecode.replace(Standard_labelname,Target_code)
#    final_execode_file.write(final_execode_code+'\n')





os.system("sed -i 's/<url>/%s/g' %s/final_execute"%(target['ip'],weblogic))
os.system("sed -i 's/<port>/%s/g' %s/final_execute"%(target['port'],weblogic))
#os.system("sed 's/<ip>/%s/'  %s"%(solr,target['ip']))


#RUN
os.system("sh %s/final_execute"%(weblogic))


#delete
os.system("rm -rf %s/final_execute"%(weblogic))


#POC_file.close()
#standard_label_file.close()

