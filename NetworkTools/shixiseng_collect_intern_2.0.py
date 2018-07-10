# -*- coding: utf-8 -*-
"""
获取并保存实习僧网站(https://www.shixiseng.com)职位的信息。
"""
import os
import re
import time
import hashlib
from urllib.request import urlopen

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont

        
class ShixisengIntern:
    def __init__(self, savepath=None):
        """
        初始化。
        
        Parameters
        ----------
        savepath: 保存路径
        """
        self.main_url = 'https://www.shixiseng.com'
        self.number_map = None

        self.headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'
        }
        
        self.savepath = savepath
        if not self.savepath:
            self.savepath = os.path.join(os.getcwd(), 'my_intern_collect.xls')
        
        # 初始化data frame
        columns = ['工作名称', '刷新时间', '工资', '城市', '学历', 
                   '实习天数', '实习月份', '职位诱惑', '具体要求', 
                   '公司名称', '公司地点', '应聘截止日期', '网址', ]
        self.df = pd.DataFrame(None, columns=columns)
    
    def get_jobs(self, job='数据', city='北京', pages=100, release_time='ft-wek'):
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
        city_code = self.get_city_code(city)
        
        if release_time not in ['ft-day', 'ft-wek', 'ft-mon']:
            raise ValueError('release_time 应为 ["ft-day", "ft-wek", "ft-mon"] 之一')
        
        page = 1
        url = '{url}/interns/st-intern_c-{c}_{r}?k={k}&p={p}'.format(
                    url=self.main_url, r=release_time, c=city_code, k=job, p=page)
        response = requests.get(url, headers=self.headers)
        
        # 获得总页数
        page_num = re.search(r'<a href=\".*?p=(.*?)\">尾页', response.text).group(1)
        page_num = min(int(page_num), int(pages))
        print('Download {} pages.'.format(page_num))
        response.close()
        
        for page in range(1, page_num + 1):
            url = '{url}/interns/st-intern_c-{c}_{r}?k={k}&p={p}'.format(
                    url=self.main_url, r=release_time, c=city_code, k=job, p=page)
            response = requests.get(url, headers=self.headers)
            links = self.get_internlinks(response, 'jobs')
            self.links_parse(links)
            response.close()
        self.save(self.savepath)
    
    def get_city_code(self, city):
        """通过页面获取城市代码"""
        if city == '全国':
            return 'None'
        pattern = re.compile(f'data-val=(.+?) > {city} </li>')
        response = requests.get(self.main_url)
        text = response.text
        response.close()
        
        try:
            city_code = re.findall(pattern, text)
        except IndexError:
            raise ValueError('不支持查询该城市：{city}')
        return city_code
        
    def get_collect(self, username, password):
        """
        爬取收藏夹中的职位信息
        
        Parameters
        ----------
        username: 用户名，用于模拟登陆。
        password: 密码，用于模拟登陆。"""
        self.login(username, password)
        
        collect_url = '{0}/my/collect'.format(self.main_url)
        response = self.session.get(collect_url, headers=self.headers)
        
        # 获得总页数
        page_num = re.search(r'<a title="第1页 / 共(\d+)页" >1</a>', response.text).group(1)
        print(f'预计下载 {page_num} 页')
        response.close()
        
        # 逐页处理
        for i in range(1, int(page_num) + 1):
            page_url = '{0}?p={1}'.format(collect_url, i)
            response = self.session.get(page_url)
            links = self.get_internlinks(response, 'collect')
            self.links_parse(links)
            response.close()
        self.save(self.savepath)
        self.session.close()
        
    def login(self, username, password):
        """模拟登陆"""
        login_info = {'username': username, 'password': self._myencode(password)}
        login_url = '{0}/user/login'.format(self.main_url)
        
        self.session = requests.Session()
        self.session.post(login_url, login_info)
    
    def get_internlinks(self, response, page_type):
        soup = BeautifulSoup(response.content, 'lxml')
        if page_type == 'jobs':
            job_list = soup.body.find(class_='position-list')
            intern_list = job_list.find_all(class_='name-box clearfix')
        elif page_type == 'collect':
            right_box = soup.body.div.find(class_='right-box')
            intern_list = right_box.div.find_all(class_='intern-name')
            
        link_list = []
        for job in intern_list:
            job_link = job.a['href']
            link_list.append(job_link)
        return link_list
    
    def links_parse(self, links):
        """逐一解析职位信息页面，提取所需信息"""
        for link in links:
            # 限制爬取速度，防止造成骚扰/被封
            wait_time = 2 * np.random.random()
            time.sleep(wait_time)
            
            intern_url = self.main_url + link
            print(f'解析页面：{intern_url}')
            intern_response = requests.get(intern_url)
            try:
                intern = self.link_parse(intern_response)
            except Exception:
                print('解析失败，跳过此页')
            intern_response.close()
            self.df = self.df.append(pd.DataFrame([intern], columns=self.df.columns), ignore_index=True)
        
    def link_parse(self, response):
        """爬取职位页面的具体信息。"""
        self.number_map = self.get_number_map(response)
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        intern = []
        intern.append(soup.body.div.find(class_='new_job_name')['title'])
        refresh_time = soup.body.div.find(class_='job_date').get_text()
        intern.append(self.translate(refresh_time))
        money = soup.body.div.find(class_='job_msg').find(class_='job_money').get_text()
        intern.append(self.translate(money))
        intern.append(soup.body.div.find(class_='job_msg').find(class_='job_position').get_text())
        intern.append(soup.body.div.find(class_='job_msg').find(class_='job_academic').get_text())
        week = soup.body.div.find(class_='job_msg').find(class_='job_week').get_text()
        intern.append(self.translate(week))
        month = soup.body.div.find(class_='job_msg').find(class_='job_time').get_text()
        intern.append(self.translate(month))
        intern.append(soup.body.div.find(class_='job_good').get_text())
        intern.append(soup.body.div.find(class_='job_detail').get_text())
        intern.append(soup.body.div.find(class_='job_com_name').get_text())
        intern.append(soup.body.div.find(class_='com_position').get_text())
        deadline = soup.body.div.find(class_='con-job deadline').find(class_='job_detail').get_text()
        intern.append(self.translate(deadline))
        intern.append(response.url)
        return intern

    def translate(self, string):
        """
        网页上职位的数字是unicode通过自定义字体显示为数字，直接存储会无法显示。
        """
        if not self.number_map:
            raise ValueError('未能生成数字映射数据，请重试。')
        
        # TODO 字体查重
        
        replace_string = string
        for key, value in self.number_map.items():
            replace_string = re.sub(key, str(value), replace_string)
        return replace_string
    
    def get_number_map(self, response):
        """
        通过字体文件获取数字的映射关系。
        """
        pattern = re.compile('@font-face \{font-family\:myFont; src\: url\(\"(.+?)\"\)\}')
        fontpath = re.search(pattern, response.text)[1]
        
        # 判断字体文件是否已获得
        # if hashlib.md5(fontpath) == self.font_md5:
        # return self.number_map
        
        font = TTFont(urlopen(fontpath))
        font_map = font.getBestCmap()
        glyph_order = font.getGlyphOrder()[2:12]
        number_map = {chr(k): v[-1]  for k, v in font_map.items() if v in glyph_order}
        return number_map
    
    @staticmethod
    def _myencode(source):
        """网站对密码进行了加密，需要进行相同操作才能提交"""
        string = []
        for i in source:
            string.append(str(ord(i))[::-1])
        encode_string = 'X'.join(reversed(string))
        return encode_string
    
    def save(self, savepath):
        """保存到文件"""
        postfix = os.path.splitext(savepath)[1]
        
        if postfix in ['.xls', '.xlsx', '.xlsm']:
            self.df.to_excel(savepath)
        elif postfix in ['.csv']:
            self.df.to_csv(savepath)        
        else:
            raise ValueError(f'文件格式{postfix}不支持。')
        print(f'保存到路径：{savepath}')

    
if __name__ == '__main__':
    savedir=os.getcwd()
    savename='intern_info.xls'
    savepath = os.path.join(savedir, savename)

    mycollect = ShixisengIntern(savepath)
    
    # 爬取职位信息
    job = '数据分析'
    city = '北京'
    mycollect.get_jobs(job=job, city=city, pages=10)
    mycollect.save(f'{job}_{city}_实习.xls')
    
    # 爬取收藏职位信息
    """
    username = 'youraccount'
    password = 'youraccount'
    mycollect.get_collect(username, password)
    """
    