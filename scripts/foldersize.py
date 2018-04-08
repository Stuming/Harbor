import os
import re
import sys


def folder_size(folder):
    """
    Calculate total size and number of files under folder.
    """
    totalsize = 0
    filenumber = 0

    for (path, dirs, files) in os.walk(folder):
        for singlefile in files:
            singlepath = os.path.join(path, singlefile)
            if not os.path.exists(singlepath):
                # prevent invalid softlink caused error
                print('File not exists: {}'.format(singlepath))
                continue
            totalsize = totalsize + os.path.getsize(singlepath)
            filenumber = filenumber + 1

    print('--'*10)
    print('{0}:'.format(folder))
    if totalsize/1024.0 < 0.01:
        print('\tsize: {0}B'.format(totalsize))
    elif totalsize/(1024*1024.0) < 0.01:
        print('\tsize: {0:.2f}KB'.format(totalsize/1024.0))
    elif totalsize/(1024*1024*1024.0) < 0.01:
        print('\tsize: {0:.2f}MB'.format(totalsize/(1024*1024.0)))
    else:
        print('\tsize: {0:.2f}GB'.format(totalsize/(1024*1024*1024.0)))
    print('\tfiles: {0}'.format(filenumber))
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

