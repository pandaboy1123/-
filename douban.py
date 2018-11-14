# 1.使用任意代理IP进行如下操作
# 2.使用requests模块进行豆瓣电影的个人用户登录操作
# 3.使用requests模块访问个人用户的电影排行榜->分类排行榜->任意分类对应的子页面
# 4.爬取需求3对应页面的电影详情数据
# 5.爬取3对应页面中滚动条向下拉动2000像素后加载出所有电影详情数据，存储到本地json文件中或者相应数据库中
# 【备注】电影详情数据包括：海报url、电影名称、导演、编剧、主演，类型，语言，上映日期，片长，豆瓣评分
import random
import re
import requests
from PIL import Image
from io import BytesIO
import lxml
from bs4 import BeautifulSoup as bs
import json
import sys
import time


def get_info(url):
    '''
    解析网页页面数据，有可能会解析失败导致文件无法保存成json
    :param url:
    :return:
    '''
    page = requests.get(url).text
    sec = random.randint(2, 6)
    print('防止禁用爬虫，程序等待%s秒' % sec)
    time.sleep(sec)
    data = {}
    data['导演'] = 'None'
    data['编剧'] = 'None'
    data['主演'] = 'None'
    data['类型'] = 'None'
    data['语言'] = 'None'
    data['上映日期'] = 'None'
    data['片长'] = 'None'
    data['海报url'] = 'None'
    data['电影名称'] = 'None'
    data['豆瓣评分'] = 'None'
    soup = bs(page, 'lxml')
    # 海报url
    poster_url = soup.find('div', {'id': 'content'}).find('a', {'class': 'nbgnbg'}).find('img')['src']
    # 电影名称
    mov_name = soup.find('div', {'id': 'content'}).find('h1').find('span').text
    language = soup.find_all('div', {'id': 'info'})
    base_info = []
    for i in language:
        base_info.append(i.text)
    # print(base_info)
    for i in base_info:
        try:
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
        except Exception as e:
            pass


    # 豆瓣评分
    score = soup.find('div', {'class', 'grid-16-8 clearfix'}).find('div', {'class': 'rating_self clearfix'}).find(
        'strong').text
    try:
        data['海报url'] = poster_url
        data['电影名称'] = mov_name
        data['豆瓣评分'] = score
    except Exception as e:
        pass
    with open('./详细信息/%s.json' % mov_name.replace(' ','').replace('：','').replace(':',''), 'w+', encoding='utf-8') as fp:
        json.dump(data, fp)


def view_bar(num):
    '''
    一个假的进度条
    :param num:
    :return:
    '''
    # rate = num / total
    # rate_num = int(rate * 100)
    r = '\r[%s%s]' % (">" * num, " " * (100 - num))
    sys.stdout.write(r)
    sys.stdout.flush()


def main_core():
    '''
    基础信息的配置
    :return:
    '''
    # 基本信息配置
    # UA配置
    header_list = [
        # 遨游
        {"user-agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
        # 火狐
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
        # 谷歌
        {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 "
                          "(KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},
    ]
    # IP段配置，如果失效了就要再去http://www.goubanjia.com/找http的ip段
    proxy_list = [
        {"http": "117.191.11.103:8080"},
        {'http': '173.249.43.105:3128'},
        {'http': '110.249.177.114:8060'},
    ]
    # 用户登录账号信息
    data = {
        'source': 'movie',
        'redir': 'http://movie.douban.com/',
        'form_email': 'XXXXXX@XX.com',
        'form_password': 'XXXXXX',
        'login': '登录',
    }
    param = {
        'type_name': '喜剧',
        'type': '24',
        'interval_id': '100:90',
        'action': '',
    }
    # 登录url
    url = 'http://www.douban.com/accounts/login'
    # 分类url
    get_url = 'http://movie.douban.com/typerank'
    # 初始化基本配置，随机选择UA和ip段
    header = random.choice(header_list)
    proxy = random.choice(proxy_list)
    session = requests.session()
    res1 = session.get(url=url, headers=header, proxies=proxy)

    # 如果产生了验证码就要解析
    try:
        page_text = res1.text
        soup = bs(page_text, 'lxml')
        cap = soup.find('div', {'class': 'item item-captcha'}).find('img')
        check_id = soup.find('div', {'class': 'captcha_block'}).find('input', {'name': 'captcha-id'})
        check_value = re.findall('value="(.*)"', str(check_id))[0]
        img_src = re.findall('src="(.*)"', str(cap))[0]
        response = requests.get(img_src)
        image = Image.open(BytesIO(response.content))
        image.show()
        check_code = input('请输入验证码>>>').strip()
        data['captcha-solution'] = check_code
        data['captcha-id'] = check_value
    except Exception as e:
        print('没有产生验证码，程序继续>>>')
    res = session.post(url=url, headers=header, data=data, proxies=proxy)
    page_text = res.text
    # +------------------------------------------------------------------+
    count_url = 'http://movie.douban.com/j/chart/top_list_count'
    count_param = {
        'type': '24',
        'interval_id': '100:90',
    }
    count_req = session.get(url=count_url, params=count_param, proxies=proxy)
    # print(type(count_req.text))
    count_dict = json.loads(count_req.text)
    total_num = count_dict['total']
    total_url = 'http://movie.douban.com/j/chart/top_list'
    total_num_list = []
    total_param = {
        'type': '24',
        'interval_id': '100:90',
        'action': "",
        'start': '0',
        'limit': total_num,
    }
    print('downloading....')
    total_req = session.get(url=total_url, params=total_param, proxies=proxy)
    print('loading....')
    for i in range(0, 101):
        time.sleep(0.1)
        view_bar(i)
    print('\n')
    total_json = json.loads(total_req.text)
    for i in total_json:
        url = i['url']
        print(url)
        get_info(url)


if __name__ == '__main__':
    main_core()