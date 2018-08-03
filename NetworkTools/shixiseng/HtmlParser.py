# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont


class HtmlParser(object):
    def __init__(self):
        """Extract new urls and data from url."""
        self.number_map = None
        self.font_hash = None
    
    def parser(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'lxml')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
    
    def _get_new_urls(self, page_url, soup):
        """Extract new urls from page_url."""
        pass
    
    def _links_parse(self, links):
        """逐一解析职位信息页面，提取所需信息"""
        for link in links:
            intern_url = self.main_url + link
            print(f'解析页面：{intern_url}')
            intern_response = requests.get(intern_url)
            try:
                intern = self._link_parse(intern_response)
            except Exception:
                print('解析失败，跳过此页')
            intern_response.close()
            self.df = self.df.append(pd.DataFrame([intern], columns=self.df.columns), ignore_index=True)
    
    def get_collect_page_num(self, response):
        if response is None:
            return None
        page_num = re.search(r'<a title="第1页 / 共(\d+)页" >1</a>', response.text).group(1)
        return page_num

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

    def parser_intern_info(self, response):
        """爬取职位页面的具体信息。"""
        self.number_map = self._get_number_map(response)
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        intern = []
        intern.append(soup.body.div.find(class_='new_job_name')['title'])
        refresh_time = soup.body.div.find(class_='job_date').get_text()
        intern.append(self._translate(refresh_time))
        money = soup.body.div.find(class_='job_msg').find(class_='job_money').get_text()
        intern.append(self._translate(money))
        intern.append(soup.body.div.find(class_='job_msg').find(class_='job_position').get_text())
        intern.append(soup.body.div.find(class_='job_msg').find(class_='job_academic').get_text())
        week = soup.body.div.find(class_='job_msg').find(class_='job_week').get_text()
        intern.append(self._translate(week))
        month = soup.body.div.find(class_='job_msg').find(class_='job_time').get_text()
        intern.append(self._translate(month))
        intern.append(soup.body.div.find(class_='job_good').get_text())
        intern.append(soup.body.div.find(class_='job_detail').get_text())
        intern.append(soup.body.div.find(class_='job_com_name').get_text())
        intern.append(soup.body.div.find(class_='com_position').get_text())
        deadline = soup.body.div.find(class_='con-job deadline').find(class_='job_detail').get_text()
        intern.append(self._translate(deadline))
        intern.append(response.url)
        return intern

    def _translate(self, string):
        """
        网页上职位的数字是unicode通过自定义字体显示为数字，直接存储会无法显示。
        """
        if not self.number_map:
            raise ValueError('未能生成数字映射数据，请重试。')
        
        replace_string = string
        for key, value in self.number_map.items():
            replace_string = re.sub(key, str(value), replace_string)
        return replace_string
    
    def _get_number_map(self, response):
        """
        通过字体文件获取数字的映射关系。
        """
        pattern = re.compile('@font-face \{font-family\:myFont; src\: url\(\"(.+?)\"\)\}')
        fontpath = re.search(pattern, response.text)[1]
        
        # 判断字体文件是否已获得
        if hash(fontpath) == self.font_hash:
            return self.number_map
        
        self.font_hash = hash(fontpath)
        font = TTFont(urlopen(fontpath))
        font_map = font.getBestCmap()
        glyph_order = font.getGlyphOrder()[2:12]
        number_map = {chr(k): v[-1]  for k, v in font_map.items() if v in glyph_order}
        return number_map
    
    def get_city_code(self, response, city):
        """通过页面获取城市代码"""
        if city == '全国':
            return 'None'
        pattern = re.compile(f'data-val=(.+?) > {city} </li>')
        html_text = response.text
        
        try:
            city_code = re.findall(pattern, html_text)[1]
        except IndexError:
            raise ValueError('不支持查询该城市：{city}')
        return city_code
    