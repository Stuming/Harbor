# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont


class HtmlParser(object):
    def __init__(self):
        """Extract new urls and data from url."""
        pass
    
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
    
    def get_intern_info(self, response):
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
        
        # TODO 字体查重
        
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
        # if hashlib.md5(fontpath) == self.font_md5:
        # return self.number_map
        
        font = TTFont(urlopen(fontpath))
        font_map = font.getBestCmap()
        glyph_order = font.getGlyphOrder()[2:12]
        number_map = {chr(k): v[-1]  for k, v in font_map.items() if v in glyph_order}
        return number_map
