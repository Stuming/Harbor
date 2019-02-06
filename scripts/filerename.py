# -*- coding: utf-8 -*-
"""
This file helps replace special word in dir structure with user-defined word.

Usage:
    In command line:
        python filerename.py dirpath srcname trgname
    In python file:
        modify path, srcname, trgname
        
Example:
    In command line:
        python filerename.py 'E:' '[Stuming]' ''
        
        
Created on Wed Feb  6 13:27:49 2019

@author: Stuming
"""

import os
import sys


def main(path, srcname, trgname):
    # Traverse dir and rename files. 
    for dirpath, dirnames, filenames in os.walk(path):
        if filenames:
            for fname in filenames:
                srcpath = os.path.join(dirpath, fname)
                trgpath = srcpath.replace(srcname, trgname)
                print('Rename {} to {}'.format(srcpath, trgpath))
                os.renames(srcpath, trgpath)
                
    print('-'*10, 'End', '-'*10)
    
    
if __name__ == '__main__':
    # Modify path, srcname, trgname if not use command line.
    path = os.getcwd()
    srcname = ''
    trgname = ''
    
    length = len(sys.argv)
    if length > 1 and length <=4:
        path = sys.argv[1]
        srcname = sys.argv[2]
        if length == 4:
            trgname = sys.argv[3]
    
    main(path, srcname, trgname)
    