#!/bin/env python3
#-*- coding: utf-8 -*-

from functools import partial
from threading import Thread
from queue import Queue
import argparse
import datetime
import requests
import logging
import atexit
import time
import os

#PATH
path = os.getcwd()
dict_local = (path+'/plugins/dict/dict.txt')

ITS_DONE = ['ITS_DONE']

Session = requests.Session()

words_q = Queue()

class COLOR:
    FAIL = '\x1b[1;31m'
    FOUND = '\x1b[1;32m'
    FORB = '\x1b[1;33m'
    INFO = '\x1b[1;34m'
    END =  '\x1b[0m'


def banner():
    '''
    print('------------------------------------------------------')
    print(f"""{COLOR.INFO}Dictionary scanning being{COLOR.END}""")
    print('------------------------------------------------------')
    '''

def end_banner():
    '''
    print('-------------------------------------------------------')
    '''

def header():
    '''
    print(" Req. time\t Status \tPath")
    print("="*54)
    '''

def get_date_time(fmt):
    return datetime.datetime.fromtimestamp(time.time()).strftime(fmt)

###
def get_file_logger(log_filename=None):

    def _get_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger

    logger = _get_logger()
    filename = log_filename if log_filename else get_date_time('%Y-%m-%d')+'.log'
    fh = logging.FileHandler(filename)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(fh)
    return logger
###

def normalize(url):
    url = url if url.endswith('/') else url+'/' # check if url is terminated by slash
    url = url if url.startswith('http') else 'http://'+url # check if url started with http
    return url


def make_requests(url, proxy, timeout, logger):

    while True:
        path = words_q.get()

        if path is ITS_DONE:
            words_q.put(ITS_DONE) # notify others its done
            return

        target_url = url + path

        status_code = Session.get(target_url, allow_redirects=False,
                                  proxies={'http': proxy, 'https': proxy},
                                  timeout=timeout).status_code

        time = get_date_time("%H:%M:%S")

        message = f'\t Code={status_code}\t{path:50.50s}'

        if status_code == 404:
            '''
            print(f'{COLOR.FORB} [*] {time}{message}{COLOR.END}', end='\r')
            '''
        elif status_code == 403:
            '''
            print(f'{COLOR.FORB} [!] {time}{message}{COLOR.END}', end='\n')
            '''
        else:
            
            print(f'{COLOR.FOUND} [+] {message}{COLOR.END}', end='\n')
            

        logger.info(f'[{status_code}] => {target_url:50.50s}')


def load_words(filename):
    with open(filename) as fd:
        for line in iter(fd.readline, ''):
            yield line.strip('\n')


def setup(words_gen):
    for word in words_gen:
        words_q.put(word)

    words_q.put(ITS_DONE) # the end of wordlist
    atexit.register(done, time.time(), words_q.qsize())
    return


def start(func, *args, **kwargs):
    t = Thread(target=func, args=args, kwargs=kwargs)
    t.start()
    return t


def done(start_time, qsize):
    """
    print('_'*54)
    print(f'Time eplapsed: {time.time() - start_time:6.4f} secs')
    print(f'Total requests: {qsize}')
    print('_'*54)
    """

def scan(url, filename, proxy=None, log_filename=None, timeout=None, threads_num=None):

    url = normalize(url)

    '''
    print(f'{COLOR.INFO} Starting at {get_date_time("%Y-%m-%d %H:%M:%S")} {COLOR.END}')
    print(f'{COLOR.INFO} Target: {url} {COLOR.END}')
    '''

    wordslist = load_words(filename)

    start(setup, wordslist) # setup queue and register

    logger = get_file_logger(log_filename)

    header()

    make_reqs = partial(make_requests, url, proxy=proxy, timeout=timeout, logger=logger)

    for _ in range(threads_num):
        start(make_reqs)


def main():
    banner()
    parser = argparse.ArgumentParser(prog="dirScanner", description="Python3.6+ is NEEDED, scan log will store in current direcotry named by date time by default")
    parser.add_argument("url", help="the target you want to scan")
    #parser.add_argument("wordlist_filename", help="the dictionary you want to use in this action", default='wordlist_of_dir.txt')
    parser.add_argument("-p", "--proxy", help="proxy address like 'socks5://127.0.0.1:8080'")
    parser.add_argument("-o", "--output", help="where the log you wnat to store")
    parser.add_argument("-t", "--timeout", help="set timeout value, default is 2 seconds", type=int, default=2)
    parser.add_argument("-n", "--threads", help="how many threads you want, default value is doule cpu counts", type=int, default=os.cpu_count()*2)
    args = parser.parse_args()
    
    params = {'url': args.url,
              'filename': dict_local,
              'proxy': args.proxy,
              'log_filename': args.output,
              'threads_num': args.threads
              }
    scan(**params)

    end_banner()

if __name__ == '__main__':
    main()