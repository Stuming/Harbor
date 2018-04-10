# -*- coding: utf-8 -*-
"""
获取并保存实习僧网站(https://www.shixiseng.com)职位的信息。
"""
import os
import re
import time
import requests
from bs4 import BeautifulSoup


class ShixisengCollect:
    def __init__(self, username, password, savepath=None):
        """
        初始化查询信息。
        
        Parameters
        ----------
            username: 账号
            password: 密码
        """
        self.login_info = {'username': username, 'password': self._myencode(password)}
        
        self.main_url = 'https://www.shixiseng.com'
        self.login_url = '{0}/user/login'.format(self.main_url)
        self.collect_url = '{0}/my/collect'.format(self.main_url)
        self.savepath = savepath
        if not self.savepath:
            self.savepath = os.path.join(os.getcwd(), 'my_intern_collect.xls')
            
        # 初始化intern_list，用作表头
        intern = dict()
        intern['job_name'] = '工作名称'
        intern['refresh_time'] = '刷新时间'
        intern['money'] = '工资'
        intern['city'] = '城市'
        intern['academic'] = '学历'
        intern['week'] = '实习天数'
        intern['month'] = '实习月份'
        intern['good'] = '职位诱惑'
        intern['detail'] = '具体要求'
        intern['com_name'] = '公司名称'
        intern['com_position'] = '公司地点'
        intern['deadline'] = '应聘截止日期'
        self.intern_list = [intern]
        
    
    def run(self):
        self.login()
        collect_response = self.session.get(self.collect_url)
        page_num = self.get_total_page_num(collect_response)
        print('Total {} pages.'.format(page_num))
        # 逐页处理
        for i in range(1, page_num + 1):
            page_url = '{0}?p={1}'.format(self.collect_url, i)
            collect_response = self.session.get(page_url)
            links = self.get_internlinks(collect_response)
            for link in links:
                time.sleep(0.5)  # 限制爬取速度，防止造成骚扰
                
                intern_url = self.main_url + link
                print('Loading {}'.format(intern_url))
                intern_response = self.session.get(intern_url)
                intern = self.link_parse(intern_response)
                self.intern_list.append(intern)
        self.save(self.savepath)
        
    def login(self):
        self.session = requests.Session()
        self.session.post(self.login_url, self.login_info)
    
    def get_total_page_num(self, response):
        """
        获取收藏页面的总页数。
        
        Return
        ------
            page_num: type: int
        """
        # 通过页面获取收藏总页数
        pattern = r'<a title="第1页 / 共(\d+)页" >1</a>'
        page_num = re.search(pattern, response.text).group(1)
        return int(page_num)
            
    def get_internlinks(self, response):
        """获取收藏页的实习职位的url."""
        soup = BeautifulSoup(response.content, 'lxml')
        right_box = soup.body.div.find(class_='right-box')
        intern_list = right_box.div.find_all(class_='intern-name')
        
        link_list = []
        for intern in intern_list:
            intern_link = intern.a['href']
            link_list.append(intern_link)
        return link_list
    
    def link_parse(self, response):
        """爬取职位页面的具体信息。"""
        intern = dict()
        soup = BeautifulSoup(response.content, 'lxml')
        
        intern['job_name'] = soup.body.div.find(class_='new_job_name')['title']
        refresh_time = soup.body.div.find(class_='job_date').get_text()
        intern['refresh_time'] = self._ncr_to_int(refresh_time)
        money = soup.body.div.find(class_='job_msg').find(class_='job_money').get_text()
        intern['money'] = self._ncr_to_int(money)
        intern['city'] = soup.body.div.find(class_='job_msg').find(class_='job_position').get_text()
        intern['academic'] = soup.body.div.find(class_='job_msg').find(class_='job_academic').get_text()
        week = soup.body.div.find(class_='job_msg').find(class_='job_week').get_text()
        intern['week'] = self._ncr_to_int(week)
        month = soup.body.div.find(class_='job_msg').find(class_='job_time').get_text()
        intern['month'] = self._ncr_to_int(month)
        intern['good'] = soup.body.div.find(class_='job_good').get_text()
        intern['detail'] = soup.body.div.find(class_='job_detail').get_text()
        intern['com_name'] = soup.body.div.find(class_='job_com_name').get_text()
        intern['com_position'] = soup.body.div.find(class_='com_position').get_text()
        deadline = soup.body.div.find(class_='con-job deadline').find(class_='job_detail').get_text()
        intern['deadline'] = self._ncr_to_int(deadline)
        
        return intern

    @staticmethod
    def _ncr_to_int(string):
        """
        网页上一些数字是Numeric character reference形式，存储时显示异常，所以替换为int数字便于保存查看。
        """
        chr_reflection = {'\uf770': 0, '\uf5fa': 1, '\uf451': 2, '\ue939': 3, 
                      '\uede7': 4, '\uf328': 5, '\ued99': 6, '\uf03b': 7, 
                      '\ue9d2': 8, '\uf5e2': 9}
        replace_string = string
        for key, value in chr_reflection.items():
            replace_string = re.sub(key, str(value), replace_string)
        return replace_string
    
    @staticmethod
    def _myencode(source):
        string = []
        for i in source:
            string.append(str(ord(i))[::-1])
        encode_string = 'X'.join(reversed(string))
        return encode_string
    
    def save(self, savepath):
        try:
            import xlwt
        except ImportError:
            raise ImportError('Install xlwt package for saving')
        
        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet')
        
        j = 0
        for i in range(1, len(self.intern_list) + 1):
            intern = self.intern_list[i-1]
            sheet.write(i, j, i)
            sheet.write(i, j + 1, intern['job_name'])
            sheet.write(i, j + 2, intern['refresh_time'])
            sheet.write(i, j + 3, intern['money'])
            sheet.write(i, j + 4, intern['city'])
            sheet.write(i, j + 5, intern['academic'])
            sheet.write(i, j + 6, intern['week'])
            sheet.write(i, j + 7, intern['month'])
            sheet.write(i, j + 8, intern['good'])
            sheet.write(i, j + 9, intern['detail'])
            sheet.write(i, j + 10, intern['com_name'])
            sheet.write(i, j + 11, intern['com_position'])
            sheet.write(i, j + 12, intern['deadline'])
        print('Saving to {}'.format(savepath))
        book.save(savepath)


if __name__ == '__main__':
    username = 'yourusername'
    password = 'yourpassword'
    savepath = 'E:\\my_intern_collect.xls'
    mycollect = ShixisengCollect(username, password, savepath)
    mycollect.run()
    