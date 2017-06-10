# -*-coding:utf-8-*-
# author : cl1330104058
# 爬取代理 IP
#

import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2716.203 Safari/537.36'
}

# 存储最终结果
result = []

def vf(pool,ip):
    try:
        response = requests.get('http://www.baidu.com', headers=headers, proxies={'http':ip}, timeout=3)
    except:
        pass
    else:
        pool.append(ip)

# 爬取 cybersyndrome
def get_cyb(result):
    browser = webdriver.PhantomJS(executable_path='D:\PhantomJS')
    browser.get('http://www.cybersyndrome.net/pla6.html')
    time.sleep(5)
    ip_a = browser.find_elements_by_class_name('A')
    ip_b = browser.find_elements_by_class_name('B')
    ip_c = browser.find_elements_by_class_name('C')
    address = []
    for ip in ip_a:
        http_a = 'http://' + ip.text
        address.append(http_a)
    for ip in ip_b:
        http_b = 'http://' + ip.text
        address.append(http_b)
    for ip in ip_c:
        http_c = 'http://' + ip.text
        address.append(http_c)
    for ip in address:
        vf(result,ip)

# 爬取西刺代理
def get_xicidaili(ip_list):
    urls = ['http://www.xicidaili.com/nn/{}'.format(n) for n in range(1,11)]
    for url in urls:
        # 其实每次抓取页面之间应该有一定的时间间隔的，但是由于要验证IP花费很多时间，就省去了这个过程
        page_data = requests.get(url,headers=headers)
        soup = BeautifulSoup(page_data.text,'lxml')
        items = soup.find_all('tr')
        items.pop(0)
        for item in items:
            ip = item.select('td:nth-of-type(2)')[0].get_text()
            port = item.select('td:nth-of-type(3)')[0].get_text()
            http = 'http://' + ip + ':' + port
            vf(ip_list,http)

get_cyb(result)
get_xicidaili(result)

print(result)