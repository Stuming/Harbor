# -*- coding: utf-8 -*-
import random

import requests


class HtmlDownloader(object):
    def __init__(self):
        """Download html from url."""
        self.main_url = 'https://www.shixiseng.com'
        self.session = None
    
    def get(self, url, session=None):
        """Download and get text from url."""
        if url is None:
            return None
        headers = {'User-Agent': self.get_random_UA()}
        
        try:
            if session:
                response = session.get(url, headers=headers)
            else:
                response = requests.get(url, headers=headers)
        except Exception as e:
            print(f'Failed to download {url}.')
            print(e.args)
            return None
        
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response
        return None
    
    @staticmethod
    def get_random_UA():
        UAlist = ['Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0', 
                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36', 
                  'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0', 
                  'Mozilla/5.0 (Unknown; Linux) AppleWebKit/538.1 (KHTML, like Gecko) Chrome/v1.0.0 Safari/538.1', 
                  'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)', 
                  'Mozilla/5.0 (SMART-TV; X11; Linux armv7l) AppleWebKit/537.42 (KHTML, like Gecko) Chromium/25.0.1349.2 Chrome/25.0.1349.2 Safari/537.42', 
                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML', 
                  'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)']
        new_ua = UAlist[random.randint(0, len(UAlist)-1)]
        return new_ua
    
    def login(self, username, password):
        """模拟登陆"""
        login_info = {'username': username, 'password': self._myencode(password)}
        login_url = '{0}/user/login'.format(self.main_url)
        
        session = requests.Session()
        session.post(login_url, login_info)
        self.session = session
    
    @staticmethod
    def _myencode(source):
        """网站对密码进行了加密，需要进行相同操作才能提交"""
        string = []
        for i in source:
            string.append(str(ord(i))[::-1])
        encode_string = 'X'.join(reversed(string))
        return encode_string
    