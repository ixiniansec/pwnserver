import requests
import threading
import time
import os
import sys

path = os.getcwd()
cache = (path+'/cache')
dict = (path + '/plugins/dict.txt')

#print(dict)
f = open(cache+'/url.cache')
tmpurl = f.read()

target_url = ('http://' + tmpurl + "/")
#print(target_url)
threads = []
thread_max = threading.BoundedSemaphore(500)

header = {
   'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
}

def scan(url):
    try:
        respon = requests.get(url, headers=header)
        if (respon.status_code == 200):
            print( '[+] ' 'CODE: [' + str(respon.status_code) + ']' + "   " +url)
    except:
        pass
    thread_max.release()

def main(file,url):
    for i in file:
        newUrl = url+i
        newUrl = newUrl.strip()
        thread_max.acquire()
        t = threading.Thread(target=scan, args=(newUrl,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    start = time.time()
    url = target_url
    director = dict
    file = open(director)
    main(file,url)
    end = time.time()
    print( ' [+]',end-start)
