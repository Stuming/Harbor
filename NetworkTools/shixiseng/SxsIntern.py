# -*- coding: utf-8 -*-
import os
from multiprocessing import Process, Queue

from URLManager import UrlManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from DataOutput import DataOutput


class SxsIntern(object): 
    def __init__(self):
        self.manger = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()
    
    def get_collect(self, username, password):
        self._login(username, password)
        
        collect_url = '{0}/my/collect'.format(self.main_url)
        response = self.session.get(collect_url, headers=self.headers)
    
    def crawl(self, root_url, save_path=None, max_amount=100):
        self.manger.add_new_url(root_url)
        while(self.manger.has_new_url() and 
              self.manger.old_url_size() < max_amount):
            try:
                new_url = self.manger.get_new_url()
                html = self.downloader.download(new_url)
                new_urls, data = self.parser.parser(new_url, html)
                self.manger.add_new_urls(new_urls)
                self.output.store_data(data)
                print('Already found {} urls'.format(self.manger.old_url_size))
            except Exception as e:
                print('Crawl failed')
        self.output.write(save_path)
        
        
if __name__ == '__main__':
    mycollect = SxsIntern()
    
    # 爬取职位信息
    job = '用户研究'
    city = '北京'
    mycollect.get_jobs(job=job, city=city, pages=100)
    
    savepath = os.path.join(os.getcwd(), f'{job}_{city}_实习.xls')
    mycollect.save(savepath)
    
    # 爬取收藏职位信息
    """
    username = 'youraccount'
    password = 'youraccount'
    mycollect.get_collect(username, password)
    """
    

    