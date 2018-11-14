'''
https://movie.douban.com/subject/5133063/
电影详情数据包括：海报url、电影名称、导演、编剧、主演，类型，语言，上映日期，片长，豆瓣评分
'''
import random
import re
import requests
from PIL import Image
from io import BytesIO
import lxml
from bs4 import BeautifulSoup as bs
import json
import math
import sys
import time

base_url = 'https://movie.douban.com/subject/1393470/'
page = requests.get(base_url)
with open('./h.html', 'w', encoding='utf-8') as f:
    f.write(page.text)
with open('./h.html', 'r', encoding='utf-8') as fp:
    sec = random.randint(2,6)
    print('防止禁用爬虫，程序等待%s秒'%sec)
    time.sleep(sec)
    data = {}
    page_text = fp.read()
    soup = bs(page_text, 'lxml')
    # 海报url
    poster_url = soup.find('div', {'id': 'content'}).find('a').find('img')['src']
    # 电影名称
    mov_name = soup.find('div', {'id': 'content'}).find('h1').find('span').text
    language = soup.find_all('div', {'id': 'info'})
    base_info = []
    for i in language:
        base_info.append(i.text)
    # print(base_info)
    for i in base_info:
        director_name = re.findall('导演:(.*)', i)[0].replace('/', ',')
        screenwriter_name = re.findall('编剧:(.*)', i)[0].replace('/', ',')
        actor_name = re.findall('主演:(.*)', i)[0].replace('/', ',')
        type_name = re.findall('类型:(.*)', i)[0].replace('/', ',')
        language = re.findall('语言:(.*)', i)[0].replace('/', ',')
        data_on = re.findall('上映日期:(.*)', i)[0].replace('/', ',')
        mov_time = re.findall('片长:(.*)', i)[0].replace('/', ',')
        data['导演'] = director_name
        data['编剧'] = screenwriter_name
        data['主演'] = actor_name
        data['类型'] = type_name
        data['语言'] = language
        data['上映日期'] = data_on
        data['片长'] = mov_time
    # 豆瓣评分
    score = soup.find('div', {'class', 'grid-16-8 clearfix'}).find('div', {'class':'rating_self clearfix'}).find('strong').text
    data['海报url'] = poster_url
    data['电影名称'] = mov_name
    data['豆瓣评分'] = score
    with open('./详细信息/%s.json'%mov_name.replace(' ','').replace('：','').replace(':',''), 'w+', encoding='utf-8') as fp:
        json.dump(data, fp)
