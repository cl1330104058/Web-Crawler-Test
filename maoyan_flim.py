# -*- coding:utf-8 -*-
#
# author : cl1330104058
#
# 爬取猫眼电影TOP100

import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient()
maoyan = client['maoiyan']
maoyan_flim = maoyan['maoyan_flim']

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

# 获取每个电影的详细信息
def get_flim(url):
    page_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(page_data.text,'lxml')
    items = soup.find_all('div',{'class':'board-item-content'})
    for item in items:
        # 影片名称
        title = item.find('p',{'class':'name'}).get_text()
        # 影片主演，去除 “主演：”
        actor = item.find('p',{'class':'star'}).get_text().strip()[3:].split(',')
        # 影片上映时间，去除上映国家与开头的“上映时间：”
        time = item.find('p',{'class':'releasetime'}).get_text()[5:15]
        # 影片评分
        rating = item.find('p',{'class':'score'}).get_text()
        data = {
            'title':title,
            'actor':actor,
            'time':time,
            'rating':rating
        }
        maoyan_flim.insert_one(data)


urls = ['http://maoyan.com/board/4?offset={}'.format(n) for n in range(0,100,10)]
# 主程序
def main():
    for url in urls:
        print('正在爬取第',urls.index(url)+1,'页')
        get_flim(url)
        time.sleep(2)
    print('爬取完毕')

main()