# -*- coding: UTF-8 -*-
import configparser
import re
import time
import os
import requests
import random
import datetime


# 登录获取cookie
import schedule
from scrapy import Selector

from public import refactoring_img, contenc_description, get_words, get_conn

path = '/www/wwwroot/apt10.com/uploads/k8h8/'

cookie = '__51vcke__JoX5b2bi347uSKwB=7aaf68b9-e05e-5987-b587-3eb9830c1fc4; __51vuft__JoX5b2bi347uSKwB=1682063686836; _tcnyl=1; ripro_notice_cookie=1; __51uvsct__JoX5b2bi347uSKwB=7; wordpress_test_cookie=WP Cookie check; PHPSESSID=q813hlkbvnk1gjne4bt6hq9fj9; wordpress_logged_in_856380da3851d8f4589b6c868b64794e=mail_80793076|1683623524|mi59nHFGNV5cUd3nNRnz4Nqb7tqghHqd1dlgGIAJrzo|0382db41ba4dab289759710ce716f248b670e09de6ecbede391d500822b952c5; __vtins__JoX5b2bi347uSKwB={"sid": "6e1d8366-c1ab-5f53-a5f6-7fe32007aa4f", "vd": 21, "stt": 5529579, "dr": 1678083, "expires": 1682415720349, "ct": 1682413920349}'
class K8H8():
    def __init__(self, n):
        self.n = n
    def log(self):
        t = random.random()
        url = f'https://www.apt10.com/login.php?m=admin&c=Admin&a=login&_ajax=1&lang=cn&t={t}'
        form_data = {
            'user_name': 'admin',
            'password': 'Qwer1234!@#$'
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
    def save_data(self,info,type_id):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.log(),
            'Origin': 'https://www.apt10.com',
            'Referer': 'https://www.apt10.com/login.php?m=admin&c=Download&a=add&typeid=68&gourl=http%3A%2F%2Flocalhost%3A93%2Flogin.php%3Fm%3Dadmin%26c%3DArchives%26a%3Dindex_archives%26typeid%3D68%26lang%3Dcn&lang=cn',
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
            ('extract_code[]', info['pwd']),
            ('addonFieldExt[content]',info['Ncontent']),#内容
            ('seo_title', info['seo_title']),
            ('seo_keywords', info['seo_keywords']),
            ('seo_description', info['seo_description']),
            ('author', '小编'),
            ('origin', '网络'),
            ('update_time',time.strftime('%Y-%m-%d+%H:%M:%S', time.localtime(time.time()))),
            ('add_time',time.strftime('%Y-%m-%d+%H:%M:%S', time.localtime(time.time()))),
            ('click', random.uniform(100,1000)),#点击数
            ('downcount', random.uniform(100,1000)),#下载数
        ]

        response = requests.post('https://www.apt10.com/login.php', params=params, headers=headers, data=data)
        if response.status_code == 200:
            print(response.text)
            return True
        return False


    def get_type_id(self,type_name):
        type_list = {'最新文章': 95, '文章栏目': 94, '网站源码': 68, 'html': 102, 'CMS模板/插件': 69, '视频教程': 70, '游戏/动漫/竞技': 96, '网络分享': 71, '企业/政府/行业': 72, '博客/个人/blog': 100, '财经/金融/区块链': 73, 'Wap/微信/APP': 99, '电影/视频/音乐': 74, '支付/建站/技术': 75, '聊天/交友/直播': 98, '小说/文章/图片': 76, '软件/下载/电脑': 77, '门户/新闻/资讯': 78, '导航/网址/查询': 79, '淘客/商城/B2B': 80, '行业/办公/系统': 97, '整站源码': 81, 'WordPress': 82, 'DEDECMS': 83, '论坛系统': 84, '苹果CMS': 85, '游戏搭建': 86, '网站搭建': 87, '微擎教程': 88, '其它教程': 89, '咨讯快报': 90, '福利资源': 91, '软件分享': 93, '修罗BBS': 103}
        type_id = type_list.get(type_name)
        return type_id

    def article_content(self,info):
        item = {}
        print(info)
        id = info[0]
        item['ncolumn'] = info[1]
        item['url'] = info[2]
        item['imgUrl'] = info[4]
        type_id = self.get_type_id(item['ncolumn'])
        if type_id:
            session = requests.Session()
            headers = {
                'authority': 'www.k8h8.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'max-age=0',
                'cookie': cookie,
                # 'referer': 'https://www.k8h8.com/11931.html',
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
            item['pwd'] = ''.join(text.xpath('//div[@class="margins"]/a/@data-clipboard-text').getall()).strip()
            down_url = text.xpath('//div[@class="margins"]/a[1]/@href').get()
            # print(down_url)
            item['bdwp_url'] = None
            if down_url:
                down_text = session.get(url=down_url,headers=headers)
                down_data = Selector(text=down_text.text).xpath('//body/script[1]/text()').get()
                item['bdwp_url'] = ''.join(re.findall(r"url = '(.*?)';",down_data))
                print(item['bdwp_url'])
            # print(bdwp_url.strip())
            # if item['title'] and item['Ncontent']:
            print('**********************************************')
            print(item)
            print('**********************************************')
            print(item['bdwp_url'])
            if item['bdwp_url']:
                item['bdwp_url'] = 'qzweb3.oss-cn-hangzhou.aliyuncs.com/' + item['bdwp_url']
                self.n += 1
                if self.save_data(item,type_id) is True:
                    return self.update_gather(id)
            else:
                return self.update_gather(id)
        print('未查询到栏目')
        return

    def get_detail_url(self):
        sql = """
        select * from cc_k8h8 where is_gather=0 limit 1
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
            return self.article_content(results[0])
        return

    def update_gather(self,id):
        sql = f"""
            update cc_k8h8 set is_gather=1 where id={id}
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
    schedule.every().day.at('09:00').do(K8H8(0).get_detail_url)  # 每天09:00运行
    while True:
        schedule.run_pending()
    # get_detail_url()