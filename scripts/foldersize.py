import os
import re


def folder_size(folder):
	"""
	Calculate size and number of files under folder.
	"""
    totalsize = 0
    filenumber = 0
    for (path, dirs, files) in os.walk(folder):
        for singlefile in files:
            totalsize = totalsize + os.path.getsize(os.path.join(path, singlefile))
            filenumber = filenumber + 1
    print('{0}:\n\tsize: {1:.2f} MB\n\tfiles: {2}'.format(folder, totalsize/(1024*1024.0), filenumber))
    return totalsize, filenumber

