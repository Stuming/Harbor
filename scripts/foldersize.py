import os
import re
import sys


def folder_size(folder):
    """
    Calculate total size and number of files under folder.
    """
    totalsize = 0
    filenumber = 0
    print("Path: {}".format(folder))

    for (path, dirs, files) in os.walk(folder):
        for singlefile in files:
            totalsize = totalsize + os.path.getsize(os.path.join(path, singlefile))
            filenumber = filenumber + 1
    print('{0}:\n\tsize: {1:.2f}MB\n\tfiles: {2}'.format(folder, totalsize/(1024*1024.0), filenumber))
    return totalsize, filenumber


if __name__ == '__main__':
    """
    Usage: python foldersize.py folderpath
    >>>python foldersize.py ./
    """
    try:
        folderpath = sys.argv[1]
    except IndexError:
        folderpath = os.getcwd()
    folder_size(folderpath)

