#-*- coding:utf-8 -*-
#
# author : cl1330104058
#
# 爬取豆瓣电影TOP250
#


import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# 创建数据库
client = MongoClient('localhoat',27017)
douban = client['douban']
douban_flim_TOP250 = douban['douban_flim_TOP250']

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2716.203 Safari/537.36'
}


def get_movie(url):
    page_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(page_data.content,'lxml')
    items = soup.select('div.item')
    for item in items:
        rank = item.em.text  # 得到电影排名
        titles = item.find_all('span',{'class':'title'})
        if len(titles) > 1:  # 得到电影的标题，用 if 判定电影是否有外国片名
            name = titles[0].get_text()
            name_en = titles[1].get_text().replace('\xa0',' ')
        else:
            name = titles[0].get_text()
            name_en = 'None'
        # 对 <div class=''bd>下的 <p> 标签切片，得到 电影的发行年代，国家，类型
        p = item.p.get_text().split('\n')[2]
        details = p.split('/')
        pub_time = details[0].strip()
        country = details[1].strip().split(' ')
        movie_classes = details[2].replace('\xa0','').split(' ')
        # 得到评分，引用的评论
        rating = item.find('span',{'class':'rating_num'}).get_text()
        cate = item .find('span',{'class':'inq'}).get_text()
        # 将得到的数据写进字典，以便存入数据库
        data = {
            'rank':rank,
            'name':name,
            'name_en':name_en,
            'rating': rating,
            'pub_time':pub_time,
            'country':country,
            'classes':movie_classes,
            'cate':cate
        }
        douban_flim_TOP250.insert_one(data)


urls = ['https://movie.douban.com/top250?start={}'.format(n) for n in range(0,250,25)]
for url in urls:
    print('正在爬取第', urls.index(url)+1, '页信息')
    get_movie(url)
    time.sleep(2)

print('爬取完毕')