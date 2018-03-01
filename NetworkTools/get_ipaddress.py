import requests
import re


def get_ipaddress(ip):
    """
        Get physical address of ip from ip138 with requests lib.
    
    Parameters
    ----------
        ip: ip address
        
    Return
    ------
        result: query result of ip. 
                '由于网络原因，查询失败！' stands for requests error.
                '无效的IP地址' stands for wrong input ip.
                or physical address of ip.
                
    Example
    -------
        ip = '123'
        print(get_ipaddress(ip))
        >> 无效的IP地址
        
        ip = '192.168.0.0'
        print(get_ipaddress(ip))
        >> 本地局域网
    """
    url = 'http://m.ip138.com/ip.asp'
    ipform = dict(ip=ip)
    try:
        r = requests.get(url, params=ipform)
    except:
        result = '由于网络原因，查询失败！'
    else:
        r.encoding = r.apparent_encoding
        result = re.search('<p class="result">本站主数据：(.+?)</p>', r.text).group(1)
        result = re.split('<br/>', result)[0]  # In order to remove <br/> in invaild ip result
    return result


if __name__ == '__main__':
    ip = '192.168.0.0'
    print(get_ipaddress(ip))
    