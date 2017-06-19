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

# 爬取豆瓣新片榜
def douban_xinpian():
    items = soup.find_all('div',{'class':'pl2'})
    for item in items:
        title = item.find('a').get_text().replace('\n','').replace(' ','')
        search = title.split('/')[0]
        rate = item.find('span',{'class':'rating_nums'}).get_text()
        link = item.find('a')['href']
        print(title,rate,link)
        get_cili(search)

# 爬取豆瓣本周口碑榜
def douban_week():
    time = soup.find('span',{'class':'box_chart_num'}).get_text()
    print('时间：',time)
    items = soup.find_all('div',{'class':'name'})
    for item in items:
        No = items.index(item) + 1
        title = item.find('a').get_text().replace('\n','').replace(' ','')
        search = title.split('/')[0]
        link = item.find('a')['href']
        print(No,title,link)
        get_cili(search)
# 获取影片磁力链接
def get_cili(title):
    url = 'http://www.diaosisou.net/list/{}/1'.format(title)
    page_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(page_data.text,'lxml')
    items = soup.find_all('div',{'class':'dInfo'})
    if len(items) == 0:
        print('找不到磁力链接')
    else:
        ls = []
        ls.append('在使用磁力前，请自行验证磁力的正确性！')
        for item in items[0:5]:
            magnet = item.find('a')['href']
            ls.append(magnet)
        print(ls)

douban_xinpian()
print('-------------------------')
douban_week()

