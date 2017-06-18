# -*-coding:utf-8-*-
#
#author: cl1330104058
#
# 爬取豆瓣电影新片榜，本周口碑榜

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

url = 'https://movie.douban.com/chart'
page_data = requests.get(url, headers=headers)
soup = BeautifulSoup(page_data.text, 'lxml')

def douban_xinpian():
    items = soup.find_all('div',{'class':'pl2'})
    for item in items:
        title = item.find('a').get_text().replace('\n','').replace(' ','')
        rate = item.find('span',{'class':'rating_nums'}).get_text()
        link = item.find('a')['href']
        print(title,rate,link)

def douban_week():
    time = soup.find('span',{'class':'box_chart_num'}).get_text()
    print('时间：',time)
    items = soup.find_all('div',{'class':'name'})
    for item in items:
        NO = items.index(item) + 1
        title = item.find('a').get_text().replace('\n','').replace(' ','')
        link = item.find('a')['href']
        print(NO,title,link)

douban_xinpian()
print('-------------------------')
douban_week()