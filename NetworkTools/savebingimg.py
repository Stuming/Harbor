# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 21:42:35 2018

Get background image of https://cn.bing.com and save it.
"""
import os
import re
import requests


def getHTMLtext(url):
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    return r.text


def getImgaddr(url, content):
    pattern = re.compile(r'g_img=\{url\: \"(.+?\.jpg)')
    imgurl = pattern.search(content).group(1)
    imgurl.replace('\\', '')
    
    imgurl = url + '/' + imgurl
    return imgurl


def saveimg(imgurl, imgpath):
    with open(imgpath, 'wb') as f:
        f.write(requests.get(imgurl).content)
    print('Saving to: {}'.format(imgpath))


def savebingimg(savedir=None):
    if savedir is None:
        savedir = os.getcwd()
    url = 'https://cn.bing.com'
    imgurl = getImgaddr(url, getHTMLtext(url))
    print('The url of bing background image is: \n{0}'.format(imgurl))
    imgpath = os.path.join(savedir, imgurl.split('/')[-1])
    saveimg(imgurl, imgpath)
    
    
if __name__ == '__main__':
    savebingimg()
