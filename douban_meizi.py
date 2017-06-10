import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient()
douban = client['douban']
douban_meuzi = douban['douban_meizi']

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Cookie':'bid=3jUKowvjCY8; ll="118221"; gr_user_id=667ffa1d-5d2a-4d03-b91c-e2f322aa4a45; ps=y; viewed="3236064_1408372_1937036_3788747_2359692_1395762_2164654_3335374_1431596_1788174"; _vwo_uuid_v2=90E1790F08DA86619CFB2E6B3E633BD5|b9bce08b5a122a89ffb8b4e35c33a208; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1496148013%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Du5IJNa_emHdZl_ChTeyjJwxqCavzA30Pblw2yBmnZTS%26wd%3D%26eqid%3Dc82c45e80006cd4100000003592d67bc%22%5D; ap=1; __utmt=1; ue="cl1330104058@163.com"; dbcl2="161472665:VmUmXTFi6dU"; ck=eot-; __utma=30149280.430951909.1493731418.1496130729.1496148254.19; __utmb=30149280.45.4.1496148580174; __utmc=30149280; __utmz=30149280.1495166553.15.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16147; _pk_id.100001.8cb4=f48b5a8a63f29048.1493730540.14.1496148597.1496130933.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __ads_session=aAuZdA3x6giq1YgPSwA='
}
# proxies = {
#     'http':'http://89.218.6.138:3128',
#     'http':'http://46.38.52.36:8081'
# }

# 从页面中解析出每个链接的地址
def get_page_link(url):
    page_data = requests.get(url,headers = headers)
    soup = BeautifulSoup(page_data.text,'lxml')
    items = soup.find_all('td',{'class':'title'})
    for item in  items:
        title = item.find('a')['title']
        link = item.find('a')['href']
        if link == 'https://www.douban.com/group/topic/103247197/':
            pass
        else:
            data = {
                'title':title,
                'link':link,
                'status':1
            }
            douban_meuzi.insert_one(data)

# 在每个页面中解析出每个图片的地址并下载
def get_image_link(url):
    if url == 'https://www.douban.com/group/topic/103093442/':
        pass
    else:
        page_data = requests.get(url,headers = headers)
        soup = BeautifulSoup(page_data.text,'lxml')
        images = soup.find_all('div',{'class':'topic-figure cc'})
        if len(images) > 0:
            title = soup.find('h1').get_text().replace('\n','').strip()
            print(title)
            for img in images:
                img_url = img.find('img')['src']
                downliad_img(img_url,'E:\\douban_meizi\\{}-{}.jpg'.format(title,images.index(img)+1))
        else:
            print('没有图片')

# 下载图片
def downliad_img(url,filename):
    page_data = requests.get(url,headers=headers)
    with open(filename,'wb') as file:
        file.write(page_data.content)
    print('下载完成')


# urls = ['https://www.douban.com/group/haixiuzu/discussion?start={}'.format(n) for n in range(0,200,25)]
#
# for url in urls:
#     get_page_link(url)
#     time.sleep(3)
# print('链接获取完成')
# print('开始下载图片')

for url in douban_meuzi.find({'status':1}):
    get_image_link(url['link'])
    douban_meuzi.update({'_id':url['_id']},{'$set':{'status':0}})
    time.sleep(3)
print('全部下载完毕')
