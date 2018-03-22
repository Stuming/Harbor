# -*- coding: utf-8 -*-
"""
Spyder Editor

This script file would print an ascii image of input image.

Parameters
----------
    file: path of input image file that will be converted.
    -o/-output: output path.
    -width: width of output ascii image, default is 80.
    -height: height of output ascii image, default is 80.
    
Usage
-----
>>>python img2ascii.py test.jpg -width 100 -height 100

"""
import argparse
from PIL import Image


def get_input():
    """
    Get input from command line, used for process.
    
    Return
    ------
        args.file: file name of input image.
        args.width: width of image, default is 80.
        args.height: height of image, default is 80.
        args.output: path of the output file.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('file')
    parser.add_argument('-o', '--output')
    parser.add_argument('--width', type=int, default=80)
    parser.add_argument('--height', type=int, default=80)
    
    args = parser.parse_args()

    return args.file, args.width, args.height, args.output

def get_char(r, g, b, alpha = 255):
    """
    Change value of pixel into char and return result.
    Input should be RGB value of a pixel and will be converted to gray.
        gray = 
    """
    length = len(ascii_char)
    unit = (256.0 + 1) / length
    
    # This convertion comes from wikipedia of word: Grayscale.
    gray = int(0.3 * r + 0.59 * g + 0.11 * b)
    return ascii_char[int(gray/unit)]


if __name__ == '__main__':
    imgfile, width, height, output = get_input()
    
    # This ascii_char comes from course of shiyanlou: https://www.shiyanlou.com/courses/370/labs/1191/document
    ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\
                      |()1{}[]?-_+~<>i!lI;:,\"^`'. ")

    im = Image.open(imgfile, 'r')
    im = im.resize((width, height), Image.NEAREST)
    
    text = ''
    for y in range(height):
        for x in range(width):
            text += get_char(*im.getpixel((x, y)))
        text += '\n'
    
    print(text)
    
    if output:
        with open(output, 'w') as f:
            f.write(text)
    