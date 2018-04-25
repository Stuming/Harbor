# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 17:28:37 2018

@author: Stuming
"""
import json
import requests


def getcomments(music_id, offset=0, total='false', limit=100):
    # Method learned from https://github.com/darknessomi/musicbox
    comment_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{0}/?rid=R_SO_4_{0}&offset={1}&total={2}&limit={3}'.format(music_id, offset, total, limit)
    header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
            }
    response = requests.get(url=comment_url, headers=header, timeout=5)
    response.raise_for_status()
    
    data = json.loads(response.text)
    hotcomments = []
    for comment in data['hotComments']:
        item = {'nickname': comment['user']['nickname'],
                'content': comment['content']}
        hotcomments.append(item)
    
    return [content['content'] for content in hotcomments]


if __name__ == '__main__':
    music_id = '516076896'
    print(getcomments(music_id))
    