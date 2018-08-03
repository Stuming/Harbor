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
    
    def get_collect_intern_urls(self, username, password):
        collect_url = '{0}/my/collect'.format(self.main_url)
        
        self.downloader.login(username, password)
        response = self.downloader.get(collect_url, session=self.downloader.session)
        page_num = self.parser.get_collect_page_num(response)
        print(f'预计下载 {page_num} 页')
        
        for i in range(1, int(page_num) + 1):
            page_url = '{0}?p={1}'.format(collect_url, i)
            response = self.downloader.get(page_url, session=self.downloader.session)
            urls = self.parser.get_intern_urls(response, 'collect')
            self.manger.add_new_urls(urls)
    
    def get_job_urls(self, job='数据', city='北京', pages=100, release_time='ft-wek'):
        """
        爬取指定的job信息
        
        Parameters
        ----------
        job: 职位信息，搜索关键字
        city: 所在城市，默认'北京'
        pages: 设定爬取多少页信息，默认为100，如果页面不足则以实际页面为准
        release_time: 发布时间，默认为'ft-wek'，即获取一周内发布的职位，具体参数为：
                        'ft-day': 一天内
                        'ft-wek': 一周内
                        'ft-mon': 一月内
        """
        # ft-day, ft-wek, ft-mon
        city_code = self.parser.get_city_code(city)
        
        if release_time not in ['ft-day', 'ft-wek', 'ft-mon']:
            raise ValueError('release_time 应为 ["ft-day", "ft-wek", "ft-mon"] 之一')
        
        page = 1
        url = '{url}/interns/st-intern_c-{c}_{r}?k={k}&p={p}'.format(
                    url=self.main_url, r=release_time, c=city_code, k=job, p=page)
        response = requests.get(url, headers=self.headers)
        
        # 获得总页数
        page_num = re.search(r'<a href=\".*?p=(.*?)\">尾页', response.text).group(1)
        page_num = min(int(page_num), int(pages))
        print(f'预计下载 {page_num} 页')
        response.close()
        
        # 逐页处理
        for page in range(1, page_num + 1):
            url = '{url}/interns/st-intern_c-{c}_{r}?k={k}&p={p}'.format(
                    url=self.main_url, r=release_time, c=city_code, k=job, p=page)
            response = requests.get(url, headers=self.headers)
            links = self._get_internlinks(response, 'jobs')
            self._links_parse(links)
            response.close()
        
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
    

    