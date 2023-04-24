# -*- coding: UTF-8 -*-
import re
import time

import requests
import random


# 登录获取cookie
import schedule
from scrapy import Selector

from zimeiti.public import refactoring_img, contenc_description, get_words, get_conn

path = '//192.168.0.15/data/SEO/images/k8h8/'

def log():
    t = random.random()
    url = f'http://192.168.0.231:8081/login.php?m=admin&c=Admin&a=login&_ajax=1&lang=cn&t={t}'
    form_data = {
        'user_name': 'admin',
        'password': 'admin'
    }
    response = requests.post(url=url,data=form_data)
    print(response.text)
    cookies = response.cookies.get_dict()
    cookies_list = []
    for k,v in cookies.items():
        cookies_list.append(k+'='+v)
    cookie = ';'.join(cookies_list)
    # print(cookie)
    return cookie


# 数据入库
def save_data(info,type_id):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': log(),
        'Origin': 'http://localhost:93',
        'Referer': 'http://localhost:93/login.php?m=admin&c=Download&a=add&typeid=68&gourl=http%3A%2F%2Flocalhost%3A93%2Flogin.php%3Fm%3Dadmin%26c%3DArchives%26a%3Dindex_archives%26typeid%3D68%26lang%3Dcn&lang=cn',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34',
        'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        'm': 'admin',
        'c': 'Download',
        'a': 'add',
        'lang': 'cn',
    }
    data = [
        ('title', info['title']),
        ('subtitle', ''),#副标题
        ('typeid', type_id),#栏目id
        ('tags', info['tag']),# 标签
        ('litpic_remote', info['imgUrl']),#缩略图
        ('remote_file[]', info['bdwp_url']),#下载链接
        ('addonFieldExt[content]',info['Ncontent']),#内容
        ('seo_title', info['seo_title']),
        ('seo_keywords', info['seo_keywords']),
        ('seo_description', info['seo_description']),
        ('author', '小编'),
        ('origin', '网络'),
        ('click', random.uniform(100,1000)),#点击数
        ('downcount', random.uniform(100,1000)),#下载数
    ]

    response = requests.post('http://192.168.0.231:93/login.php', params=params, headers=headers, data=data)
    if response.status_code == 200:
        return True
    return False


def get_type_id(type_name):
    type_list = {'企业/政府/行业': '72', '财经/金融/区块链': '73', '电影/视频/音乐': '74', '支付/建站/技术': '75', '小说/文章/图片': '76', '软件/下载/电脑': '77', '门户/新闻/资讯': '78', '导航/网址/查询': '79', '淘客/商城/B2B': '80', '整站源码': '81', 'WordPress': '82', 'DEDECMS': '83', '论坛系统': '84', '苹果CMS': '85', '游戏搭建': '86', '网站搭建': '87', '微擎教程': '88', '其它教程': '89', '咨讯快报': '90', '福利资源': '91', '网赚分享': '92', '软件分享': '93'}
    type_id = type_list.get(type_name)
    return type_id

def article_content(info):
    item = {}
    print(info)
    id = info[0]
    item['ncolumn'] = info[1]
    item['url'] = info[2]
    item['imgUrl'] = info[4]
    type_id = get_type_id(item['ncolumn'])
    if type_id:
        session = requests.Session()
        headers = {
            'authority': 'www.k8h8.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '__51vcke__JoX5b2bi347uSKwB=7aaf68b9-e05e-5987-b587-3eb9830c1fc4; __51vuft__JoX5b2bi347uSKwB=1682063686836; _tcnyl=1; ripro_notice_cookie=1; PHPSESSID=q24he9d38vjd3o21rafs6vfm11; wordpress_logged_in_856380da3851d8f4589b6c868b64794e=mail_80793076|1683273320|CX7asfk9APXZ3O7KwgHxkAkUQUmDZnrYvYZI5ZfFzvZ|90798aa8dab5f660d7116e70e8aa9414dc39ef10b7b679b9c93c9181dcaf54e8; __51uvsct__JoX5b2bi347uSKwB=2; __vtins__JoX5b2bi347uSKwB={"sid": "25cdd9e0-ca51-53a4-ae35-f8dcd269b265", "vd": 2, "stt": 13986, "dr": 13986, "expires": 1682067836545, "ct": 1682066036545}',
            'referer': 'https://www.k8h8.com/11931.html',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        }
        response = session.post(url=item['url'],headers=headers)
        text = Selector(text=response.text)
        item['title'] = text.xpath('//div[@class="article-title"]/h1/text()|//h1[@class="entry-title"]/text()').get()
        y_content = text.xpath('//div[contains(@class,"entry-content")]/*').getall()[:-3]
        if y_content:
            item['Ncontent'] = refactoring_img(''.join(y_content),response.url,path)
            # print(item['Ncontent'])
            item['description'] = contenc_description(item['Ncontent'])
            item['tag'] = get_words(item['Ncontent'])
        item['seo_title'] = text.xpath('//title/text()').get()
        item['seo_keywords'] = text.xpath('//meta[@name="keywords"]/@content').get()
        item['seo_description'] = text.xpath('//meta[@name="description"]/@content').get()
        item['pwd'] = ''.join(text.xpath('//div[@class="margins"]/a/@data-clipboard-text').getall())
        down_url = text.xpath('//div[@class="margins"]/a[1]/@href').get()
        # print(down_url)
        item['bdwp_url'] = None
        if down_url:
            down_text = session.get(url=down_url,headers=headers)
            down_data = Selector(text=down_text.text).xpath('//body/script[1]/text()').get()
            item['bdwp_url'] = ''.join(re.findall(r"url = '(.*?)';",down_data))
        # print(bdwp_url.strip())
        # if item['title'] and item['Ncontent']:
        if save_data(item,type_id) is True:
            return update_gather(id)
        return
    print('未查询到栏目')
    return

def get_detail_url():
    sql = """
    select * from cc_k8h81 where is_gather=0 limit 5
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    # print(results)
    # print(type(results))  # 返回<class 'tuple'> tuple元组类型
    conn.commit()
    cur.close()
    conn.close()
    print(results)
    if len(results)>0:
        for res in results:
            article_content(res)
    return

def update_gather(id):
    sql = f"""
        update cc_k8h81 set is_gather=1 where id={id}
        """
    conn = get_conn()
    cur = conn.cursor()
    results = cur.execute(sql)
    # print(results)
    # print(type(results))  # 返回<class 'tuple'> tuple元组类型
    conn.commit()
    cur.close()
    conn.close()
    print(results)
    return

if __name__ == '__main__':
    """每周手动更新一次k8h8的cookie"""
    schedule.every().day.at('09:00').do(get_detail_url)  # 每天10:30运行
    while True:
        schedule.run_pending()