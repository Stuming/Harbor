# -*- coding: utf-8 -*-


class UrlManager(object):
    def __init__(self):
        """
        Manage urls. 
        
        Attributes
        ----------
        new_urls: a set of urls that are not accessed yet. 
        old_urls: a set of urls that already accessed. 
        """
        self.new_urls = set()
        self.old_urls = set()
    
    def has_new_url(self):
        """Return True if has new url, else False."""
        return self.new_url_size() != 0
    
    def get_new_url(self):
        """Get a new url from new_urls and move the url to old_urls."""
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
    
    def add_new_url(self, url):
        """Add an url to new_urls if it is new.
        
        Parameters
        ----------
        url: url link.
        """
        if url is None:
            return 
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    
    def add_new_urls(self, urls):
        """Add urls to new_urls.
        
        Parameters
        ----------
        urls: a set of url."""
        if urls is None or len(urls) == 0:
            return 
        for url in urls:
            self.add_new_url(url)
    
    def new_url_size(self):
        """Get size of new_urls."""
        return len(self.new_urls)
    
    def old_url_size(self):
        """Get size of old_urls."""
        return len(self.old_urls)

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
        city_code = self._get_city_code(city)
        
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
            print(f'获取列表页：{url}')
            response = requests.get(url, headers=self.headers)
            links = self._get_internlinks(response, 'jobs')
            self._links_parse(links)
            response.close()