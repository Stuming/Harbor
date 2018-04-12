# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 16:16:51 2018

Usage:
    python image_resize_batch.py dirpath width height
    
    Resize all images(*.jpg) under dirpath into (width, height) size.
    If you want to make width(height) changed the same proportion as 
        height(width), input 0 for width(height)

    >>># python image_resize_batch.py dirpath width height
    >>>python image_resize_batch.py ./ 700 0

@author: Administrator
"""
import os
import sys
from PIL import Image


def image_resize(imgpath, *args):
    """Resize image in imgpath and save to the same dir."""
    print('Loading {}'.format(imgpath))
    img = Image.open(imgpath)
    origin_size = img.size
    print('Size of image: {}.'.format(origin_size))
    width, height = args
    
    if width < 0 or height < 0:
        show_usage()
        raise ValueError('Input width and height cannot be negative number.')
        sys.exit()
    if height == 0 and width == 0:
        print('Keep image size unchanged.')
        sys.exit()
    
    if height == 0:
        height = int(width / origin_size[0] * origin_size[1])
    if width == 0:
        height = int(height)
        width = int(height / origin_size[1] * origin_size[0])
        
    new_size = (width, height)
    resized_img = img.resize(new_size)
    img_root, img_ext = os.path.splitext(imgpath)
    resized_imgpath = img_root + '_{0}x{1}'.format(*new_size) + img_ext
    print('Saving {}'.format(resized_imgpath))
    resized_img.save(resized_imgpath)
    
    
def find_imgfiles(dirpath):
    """Find all image files under dirpath."""
    files = os.listdir(dirpath)
    imgfiles = [os.path.join(dirpath, file) for file in files if file.endswith('.jpg')]
    print('Finding images: ')
    print('\n'.join(imgfiles))
    print('--' * 10)
    return imgfiles


def show_usage():
    print('Usage: \n\tpython image_resize_batch.py dirpath width height\n')
    print('\tResize all images(*.jpg) under dirpath into (width, height) size.')
    print('\tIf you want to make width(height) changed the same proportion as ')
    print('\t\theight(width), input 0 for width(height)\n')
    print('\t>>># python image_resize_batch.py dirpath width height')
    print('\t>>>python image_resize_batch.py ./ 700 0')
    
    
def main():
    try:
        dirpath = sys.argv[1]
        width, height = [int(i) for i in sys.argv[2:]]
    except ValueError:
        show_usage()
        sys.exit()
    
    imgfiles = find_imgfiles(dirpath)
    for imgpath in imgfiles:
        image_resize(imgpath, width, height)


if __name__ == '__main__':
    main()
    