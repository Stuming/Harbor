# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 10:01:24 2018

@author: Stuming
"""
import os
import sys
import requests
from bs4 import BeautifulSoup


UA_address = dict(UA_Chorme = 'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/', 
                 UA_Linux = 'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/linux/', 
                 UA_Windows = 'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/', 
                 UA_Mac = 'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/mac/', 
                 UA_Android = 'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/android/')


class BuildUAPool:
    def __init__(self, ua_number=10, savepath=None):
        """
        Get ua from predefined url, and saved into file.
        
        Parameters
        ----------
            ua_number: the number of getting ua, default is 10.
            savepath: file path that saves ua_list into, default is default is None, 
                      means saving into 'UAList.txt' under current working dir.
        """
        self.ua_number = int(ua_number)
        if self.ua_number <= 0:
            raise ValueError('\'ua_number\' should be a postive int.')
        if savepath is None:
            savepath = os.path.join(os.getcwd(), 'UAList.txt')
        
        platform = sys.platform
        if platform == 'linux' or platform == 'linux2':
            self.ua_url = UA_address['UA_Linux']
            ua_default = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'
        elif platform == 'darwin':
            self.ua_url = UA_address['UA_Mac']
            ua_default = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko)'
        elif platform == 'win32' or platform == 'win64':
            self.ua_url = UA_address['UA_Windows']
            ua_default = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        else:
            self.ua_url = UA_address['UA_Chorme']
            ua_default = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        self.headers = {'user-agent': ua_default}
        
        self.request_ua()
        self.save_to_file(savepath)
    
    def request_ua(self):
        """
        Get ua list from url, and saved in self.ua_list.
        """
        ua_list = []
        page = self.get_reponse(self.headers)
        pagesoup = BeautifulSoup(page.text, 'lxml')
        ua_rawlist = pagesoup.body.find(class_='content-base').find_all(class_='useragent')
        for ua in ua_rawlist:
            ua_list.append(ua.get_text())
            self.ua_number -= 1
            if self.ua_number == 0:
                break
        ua_list[0] = '# {}'.format(ua_list[0])  # string: 'User agent'.
        self.ua_list = ua_list
    
    def save_to_file(self, savepath=None):
        """
        Save ua_list into file for further usage.
        
        Parameters
        ----------
            savepath: file path that saves ua_list into.
        """
        with open(savepath, 'w') as f:
            f.writelines([ua+'\n' for ua in self.ua_list])
        print('Saving UAList to {}'.format(savepath))
    
    def get_reponse(self, headers=None):
        """
        Get reponse from ua_url.
        """
        if headers is None:
            headers = self.headers
        page = requests.get(self.ua_url, headers=headers)
        page.raise_for_status()
        return page
    
    def show_vaildUAaddress(self):
        """
        Show the vaild UA address, which means where to request ua_list.
        """
        print('Vaild UA address: ')
        for key, value in UA_address.items():
            print('{}: {}'.format(key, value))
        

if __name__ == '__main__':
    ua = BuildUAPool()
    