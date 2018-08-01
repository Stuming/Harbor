#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 20:13:31 2018

@author: stuming
"""

import os, time, random
from multiprocessing import Process, Queue


def proc_write(q, urls):
    print(f'Process({os.getpid()}) is writing...')
    for url in urls:
        q.put(url)
        print(f'put {url} to queue...')
        time.sleep(random.random())
def proc_read(q):
    print(f'Process({os.getpid()}) is reading...')
    while True:
        url = q.get(True)
        print(f'Get {url} from queue')


if __name__ == '__main__':
    q = Queue()
    proc_w1 = Process(target=proc_write, args=(q, ['url1', 'url2', 'url3']))
    proc_w2 = Process(target=proc_write, args=(q, ['url4', 'url5', 'url6']))
    proc_r1 = Process(target=proc_read, args=(q,))
    
    proc_w1.start()
    proc_w2.start()
    
    proc_r1.start()
    
    proc_w1.join()
    proc_w2.join()
    proc_r1.terminate()
    