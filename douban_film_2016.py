# -*- coding:utf-8 -*-
# author: cl1330104058
# 抓取豆瓣电影2016榜单，并存入 MongoDB

import time
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
douban = client['douban']
douban_film = douban['douban_film']

urls = ['https://movie.douban.com/ithil_j/activity/movie_annual2016/widget/{}'.format(n) for n in range(1, 73)]

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2716.5 Safari/537.36'
}


# 得到返回的 JSON 内的需要的信息
def get_movie(url):
    page_data = requests.get(url, headers=headers)
    page_data = page_data.json()  # 因为返回的是 JSON ，所以使用 .json() 函数
    if page_data['res']['kind_cn'] == 'Top 10':  # 如果页面是关于电影TOP10的，运行下列代码
        # 电影的奖项
        title = page_data['res']['payload']['title'].split('|')
        # 电影名称
        name = page_data['res']['subject']['title']
        # 电影评分
        rating = page_data['res']['subject']['rating']
        # 引用的电影评论
        cate = page_data['res']['payload']['description']
        print('本条信息爬取完毕')
        # 写入字典，存入数据库
        data = {
            'title': title[0] + title[1],
            'movie_name': name,
            'rating': rating,
            'cate': cate
        }
        douban_film.insert_one(data)
    elif page_data['res']['kind_cn'] == '人物': # 如果页面是关于人物的，运行下列代码
        title = page_data['res']['payload']['title'].split('|')
        name = []
        for n in range(0, 10):
            name.append(page_data['res']['people'][n]['name'])
        print('本条信息爬取完毕')
        # 写入字典，存入数据库
        data = {
            'title': title[0] + title[1],
            'name': name
        }
        douban_film.insert_one(data)
    elif page_data['res']['kind_cn'] == 'TOP 5': # 如果页面是关于电影TOP5 的，运行下列代码
        title = page_data['res']['payload']['title']
        name = page_data['res']['subject']['title']
        star = page_data['res']['subject']['rating']
        description = page_data['res']['payload']['description']
        print('本条信息爬取完毕')
        # 写入字典，存入数据库
        data = {
            'title': title,
            'movie_name': name,
            'star': star,
            'description': description
        }
        douban_film.insert_one(data)
    elif page_data['res']['kind_cn'] == '逝者': # 如果页面是关于2016逝者的，运行下来代码
        title = page_data['res']['payload']['title'].split('|')
        description = page_data['res']['payload']['description']
        # 写入字典，存入数据库
        people_list = []
        for n in range(0, 9):
            people = {
                # 逝者中文姓名
                'name': page_data['res']['people'][n]['name'],
                # 逝者英文姓名
                'name_en': page_data['res']['people'][n]['name_en'],
                # 逝者职业
                'profession': page_data['res']['people'][n]['profession'],
                # 逝者年龄
                'age': page_data['res']['people'][n]['age']
            }
            people_list.append(people)
        print('本条信息爬取完毕')
        data = {
            'title': title[0] + title[1],
            'description': description,
            'people': people_list
        }
        douban_film.insert_one(data)
    else:
        print('没有信息可爬')


# 主程序，从列表内取出网址，爬取
def main():
    for url in urls:
        print('正在爬取第', urls.index(url) + 1, '条信息')
        get_movie(url)
        time.sleep(2)
    print('全部信息爬取完毕')


main()
