# -*- coding: utf-8 -*-
import time
import random

import requests


class HtmlDownloader(object):
    def __init__(self, user_agent=None):
        """Download html from url."""
        self.main_url = 'https://www.shixiseng.com'
        self.number_map = None
        
        if user_agent is None:
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0'
        self.headers = {'User-Agent': user_agent}
        
        # 初始化data frame
        columns = ['工作名称', '刷新时间', '工资', '城市', '学历', 
                   '实习天数', '实习月份', '职位诱惑', '具体要求', 
                   '公司名称', '公司地点', '应聘截止日期', '网址', ]
        
    
    def download(self, url):
        """Download and get text from url."""
        if url is None:
            return None
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None


    def _links_parse(self, links):
        """逐一解析职位信息页面，提取所需信息"""
        for link in links:
            # 限制爬取速度，防止造成骚扰/被封
            wait_time = 2 * random.random()
            time.sleep(wait_time)
            
            intern_url = self.main_url + link
            print(f'解析页面：{intern_url}')
            intern_response = requests.get(intern_url)
            try:
                intern = self._link_parse(intern_response)
            except Exception:
                print('解析失败，跳过此页')
            intern_response.close()
            self.df = self.df.append(pd.DataFrame([intern], columns=self.df.columns), ignore_index=True)
    
    def get_collect(self, username, password):
        """
        爬取收藏夹中的职位信息
        
        Parameters
        ----------
        username: 用户名，用于模拟登陆。
        password: 密码，用于模拟登陆。"""
        self._login(username, password)
        
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
            links = self._get_internlinks(response, 'collect')
            self._links_parse(links)
            response.close()
        self.session.close()
    
    def _login(self, username, password):
        """模拟登陆"""
        login_info = {'username': username, 'password': self._myencode(password)}
        login_url = '{0}/user/login'.format(self.main_url)
        
        self.session = requests.Session()
        self.session.post(login_url, login_info)
    
    def _get_internlinks(self, response, page_type):
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
        
    @staticmethod
    def _myencode(source):
        """网站对密码进行了加密，需要进行相同操作才能提交"""
        string = []
        for i in source:
            string.append(str(ord(i))[::-1])
        encode_string = 'X'.join(reversed(string))
        return encode_string
    
    def _get_city_code(self, city):
        """通过页面获取城市代码"""
        if city == '全国':
            return 'None'
        pattern = re.compile(f'data-val=(.+?) > {city} </li>')
        response = requests.get(self.main_url)
        text = response.text
        response.close()
        
        try:
            city_code = re.findall(pattern, text)[1]
        except IndexError:
            raise ValueError('不支持查询该城市：{city}')
        return city_code