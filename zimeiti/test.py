# -*- coding:utf-8 -*-
import html
import random
import re
import time
from urllib.parse import urljoin, urlencode

from scrapy import Selector
import requests
from lxml import etree
import urllib3
import cloudscraper
# from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from zimeiti.public import down_img, is_exists, refactoring_img, contenc_description, get_words, execute

urllib3.disable_warnings()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}


# url = 'https://www.lishi.net/wp-admin/admin-ajax.php'
# data = {'action': 'wpcom_load_posts',
#         'page': '50',
#         'taxonomy': 'category',
#         'id': '141',
#         'type': 'default',
#         'attr':'',
#         'order': ''}
# response = requests.post(url=url,data=data)
# print(response.status_code)
# print(response.text)

# lanmu = {'先秦秦汉历史': '160', '魏晋南北朝': '161', '隋唐元明清': '162', '民国历史': '163', '现代史': '164', '亚洲历史': '121', '美洲历史': '126', '欧洲历史': '124', '非洲历史': '137', '大洋洲及南极洲历史': '140', '中国人物': '141', '世界人物': '142', '神话人物': '143', '影视剧人物': '144', '焦点事件': '120', '中国事件': '157', '外国事件': '158', '历史解秘': '147', '野史趣闻': '5', '战争': '155', '传统文化': '148', '西方文化': '149', '神话故事': '151', '历史典故': '150', '文史百科': '180', '世界地理': '153', '中国地理': '152'}
# for k,v in lanmu.items():
#         print(k,v)

# import emoji
#
# test_str = """服务周到，性价比高，量还多，强烈推荐😍😍😍"""
# result = emoji.demojize(test_str)
# result = re.sub(':\S+?:', '', result)
# print(result)
# url = 'https://inews.gtimg.com/newsapp_bt/0/13717455031/1000'
# response = requests.get(url=url)
# # print(response.content)
# open('//192.168.0.15/data/SEO/images/1.jpg','wb').write(response.content)

# wei = '/info/17150_10.html'
# s_url = 'https://www.gushi365.com/info/17150.html'

# w_url = urljoin(s_url, wei)
# print(w_url)
# page = re.findall(r'_(.*?)\.html',w_url)[0]
# print(page)
# p = 2
# d_url = re.sub(r'_(.*?)\.html',f'_{p}.html',w_url)
# print(d_url)

# url = 'https://www.etgushi.com/jdth/7937_2.html'
# resp = requests.get(url)
# resp.encoding = resp.apparent_encoding
# html_text = Selector(text=resp.text)
# tx = html_text.xpath('//div[@id="ny"]/*').getall()
# print(tx)


# resp = requests.get(url='http://www.zhuaidei.com/news/18149_2.html')
# resp.encoding = resp.apparent_encoding
# html_text = etree.HTML(resp.text)
# tx = html_text.xpath('//div[@class="articleContent"]/*')
# for t in tx:
#     ps = html.unescape((etree.tostring(t)).decode('utf-8'))
#     print(ps)

# a = 'https://www.popao.cn/shuoshuo/list_4_3.html'
# print(re.findall(r'_._(.*?)\.html',a)[0])

# url = 'https://www.6mj.com/news/mingnv/11932144548E2EFFJGCD0864D399IF.htm'
# # resposne = requests.get(url=url,verify=False)
# # resposne.encoding = resposne.apparent_encoding
# # resposne = Selector(text=resposne.text)
# # text = resposne.xpath('//div[@class="meta"]/p').getall()[2:]
# # print(text)
# print(url[:9:2])


# a = """<p align="left" style="line-height: 150%"><span style="FONT-SIZE: 12pt">\r\n<p style="line-height: 200%"><span style="font-size: medium">\u3000\u3000从前有个师傅带了两个徒弟，临终时把两个徒弟叫到床前指着身边放的东西，上气不接下气吃力地说：“我已不行了，留给你两的东西也不多，只有这两件，你没人各拿一件。”说完就闭上眼睛、咽了气。</span></p>"""
#
# b = re.sub('\s',' ',a)
# print(a)
# print(b)

# li = 'background-image:url(http://www.rrlady.com/uploads/allimg/180302/1_0302152533c06.gif)'
# fmt_url = re.findall(r'\((.*?)\)',li)[0]
# print(fmt_url)
#
# a = '导读：全方位生活护理婴幼儿用品专门企业Medience（保宁米迪恩）的代表品牌B&B，在11日推出了3种婴幼儿护肤产品，预计在5月末登录天猫国际的保宁海外旗舰店开始售卖。...'
# print(a.split('导读：')[-1])

# url = 'http://www.rrlady.com/meirong/xiufa/18592.html'
#
# res = requests.get(url)
# resp = Selector(text=res.text)
# print(resp.xpath('//div[@class="post-content"]'))

# a = 'd9d1b656b7_1566874918910228.jpg?x-image-process=image.jpg?:/\*<>'
#
# print(re.sub(r'[\\/:*?"<>|]','',a))
# class PDTOMYSQL:
#     def __init__(self,df):
#
#         self.host = '127.0.0.1'
#         self.user = 'root'
#         self.port = '3306'
#         self.db = 'cc_11'
#         self.password = 'root'
#         self.tb = 'stock1'
#         self.df = df
#
#         sql = 'select * from '+self.tb
#         conn = create_engine('mysql+pymysql://'+self.user+':'+self.password+'@'+self.host+':'+self.port+'/'+self.db)
#         df.to_sql(self.tb, con=conn, if_exists='replace')
#         self.pdata = pd.read_sql(sql,conn)
#     def show(self):#显示数据集
#         return print(self.pdata)
#
# data = {
#     'state':['Ohio','Ohio','Ohio','Nevada','Nevada'],
#     'year':[2000,2001,2002,2001,2002],
#     'pop':[1.5,1.7,3.6,2.4,2.9]
# }
# #把data转换成dataframe数据
# frame = pd.DataFrame(data)
# t = PDTOMYSQL(
#     df=frame)
# t.show()


# browser = cloudscraper.create_scraper()
# data = browser.get(url='https://ai-bot.cn/',headers={'Referer':'https://ai-bot.cn/'})
#
# print(data.status_code)
# print(data.text)
# import requests
# from http import cookiejar
# from requests.sessions import RequestsCookieJar
# # 创建Cookie池
# cookie_jar = cookiejar.CookieJar()
# cookie_processor = requests.cookies.RequestsCookieJar()
# session = requests.session()
# session.cookies = cookie_jar
#
# # 设置请求头
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
#     'Referer': 'https://ai-bot.cn/',
# }
#
# # 发送请求
# response = session.get('https://ai-bot.cn/', headers=headers)
# print(response.status_code)
# print(response.text)


# coo = [{'domain': '.ai-bot.cn', 'expiry': 1680511792, 'httpOnly': True, 'name': '__cf_bm', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'Gp8oDCRr9sYnIcbfu0T3yGmtEL8mhdTMEE9UNscHyWc-1680509991-0-AcDiuawDfWpJ19uKE4R94djwYRFazi5fAMuZhwn4xwHU7VIkvmF/RtkT0CwxHJ4AN/HlpMqkBtBfWv5MN/fcnB1Ph6JxlYv3PR/UCgsnKzZmN4RF6THo0SO20MQKUbTWUA=='}, {'domain': '.ai-bot.cn', 'expiry': 1712045980, 'httpOnly': True, 'name': 'cf_clearance', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'NgoC4CRYtK85dzZyJlG9zsT0kG4ETfYN.27KRiZpENs-1680509978-0-160'}, {'domain': '.ai-bot.cn', 'expiry': 1715069984, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.1.69386245.1680509984'}, {'domain': '.ai-bot.cn', 'httpOnly': False, 'name': 'Hm_lpvt_55906d9c57011d694d405f963a90648b', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1680509991'}, {'domain': '.ai-bot.cn', 'expiry': 1712045991, 'httpOnly': False, 'name': 'Hm_lvt_55906d9c57011d694d405f963a90648b', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1680509991'}, {'domain': '.ai-bot.cn', 'expiry': 1715069984, 'httpOnly': False, 'name': '_ga_D5V8ZDEBC0', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1680509984.1.0.1680509984.0.0.0'}]
# keys = []
# values = []
# for c in coo:
#     keys.append(c['name'])
#     values.append(c['value'])
# print(dict(zip(keys,values)))

# def jquery_mock_callback():
#     jQuery_Version = "3.6.0"
#     return "jQuery" + (jQuery_Version + str(random.random())).replace(".", "") + "_" + str(
#         int(round(time.time() * 1000)) - 1000)  # 版本号只留下数字，加上随机值与13位时间戳
#
#
# pamars = {
#     'callback': jquery_mock_callback(),
#     'page': 1,
#     'type': 'json',
#     '_': str(int(time.time()))
# }
#
# print(urlencode(pamars))
# num = 'events/luntan1/.html'
# a = re.sub("\D", "", num)
# print(a)

# a = "downLink('725831778');bear_countone('725831778','8001');_hmt.push(['_trackEvent','beardown','PC','顶部立即下载'])"
# print(re.findall(r"downLink\('(.*?)'\)",a))

# resp = requests.get('https://www.bear20.com/window/4531/473302453.html')
# text = Selector(text=resp.text)
# content = text.xpath('//div[@class="content"]').getall()
# print(content[0].split('<div id="lsbb"')[0])

import requests

cookies = {
    'tt_webid': '7216896502097331770',
    '_ga': 'GA1.1.1879555226.1680314668',
    '__ac_signature': '_02B4Z6wo00f01dkQYbwAAIDAuhqh12sHIj3ZMGUAABJ6fd',
    '__ac_referer': 'https://www.toutiao.com/',
    '_tea_utm_cache_4916': 'undefined',
    '_S_DPR': '1',
    '_S_IPAD': '0',
    's_v_web_id': 'verify_lgki81z1_RLAE5DAM_5eOW_4mcd_9Blc_hJtQ9bjKqH9Y',
    'notRedShot': '1',
    'ttwid': '1%7CR6oJ8LfbwOBgFcz83MsG_u717WWRjqakhVy2TSRnCM8%7C1681717364%7Cd73e022bf83127ccf08b767c1df1066e0f25fcd660cb97d239af90913e533828',
    '_ga_QEHZPBE5HH': 'GS1.1.1681715831.2.1.1681717623.0.0.0',
    '_S_WIN_WH': '1920_969',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'tt_webid=7216896502097331770; _ga=GA1.1.1879555226.1680314668; __ac_signature=_02B4Z6wo00f01dkQYbwAAIDAuhqh12sHIj3ZMGUAABJ6fd; __ac_referer=https://www.toutiao.com/; _tea_utm_cache_4916=undefined; _S_DPR=1; _S_IPAD=0; s_v_web_id=verify_lgki81z1_RLAE5DAM_5eOW_4mcd_9Blc_hJtQ9bjKqH9Y; notRedShot=1; ttwid=1%7CR6oJ8LfbwOBgFcz83MsG_u717WWRjqakhVy2TSRnCM8%7C1681717364%7Cd73e022bf83127ccf08b767c1df1066e0f25fcd660cb97d239af90913e533828; _ga_QEHZPBE5HH=GS1.1.1681715831.2.1.1681717623.0.0.0; _S_WIN_WH=1920_969',
    'Referer': 'https://so.toutiao.com/search?dvpf=pc&source=pagination&keyword=%E9%87%8D%E5%BA%86%E6%97%85%E6%B8%B8&pd=information&action_type=pagination&page_num=2&search_id=202304171543102078D8317CE71FDAF7BA&from=news&cur_tab_title=news',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'dvpf': 'pc',
    'source': 'pagination',
    'keyword': '重庆旅游',
    'pd': 'information',
    'action_type': 'pagination',
    'page_num': '3',
    'search_id': '202304171543102078D8317CE71FDAF7BA',
    'from': 'news',
    'cur_tab_title': 'news',
}

response = requests.get('https://so.toutiao.com/search', params=params, cookies=cookies, headers=headers)