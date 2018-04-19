# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 21:10:51 2018

@author: Stuming
"""
from threading import Thread


class Cal(object):
    def __init__(self, start, end):
        self.result = 0
        self.start = start
        self.end = end
    
    def map(self):
        for i in range(self.start, self.end):
            self.result += i
    
    def reduce(self, other):
        self.result += other.result


def generate_workers(data):
    for index in range(1, len(data)):
        cal = Cal(data[index-1], data[index])
        yield cal


def generate_threads(workers):
    for worker in workers:
        thread = Thread(target=worker.map)
        thread.start()
        yield thread


def main():
    print('Adding from 1 to 100')
    data = [num for num in range(1, 102, 10)]
    
    workers = list(generate_workers(data))
    threads = list(generate_threads(workers))
    
    for thread in threads:
        thread.join()
    
    start = workers[0]
    for worker in workers[1:]:
        start.reduce(worker)
    
    print('Result: {}'.format(start.result))
    assert start.result == sum(range(1, 101))  # 5050


if __name__ == '__main__':
    main()
    