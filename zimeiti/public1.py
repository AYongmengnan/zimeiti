# -*- coding:utf-8 -*-
"""
公用方法：
下载文章中的图片内容
获取关键字、标签、简介
入库前判断数据是否存在
"""
import hashlib
import os
import random
import re
import time

import emoji
import pymysql
import requests
from urllib import parse
import urllib3
from lxml import etree
import jieba
import pandas as pd
from w3lib.html import remove_tags, remove_comments, remove_tags_with_content

urllib3.disable_warnings()


# 取出内容中所有图片地址@src
def refactoring_img(article, prefix, path):
    images_list = []
    if not article:
        return article, []
    html = etree.HTML(article)
    imglist = html.xpath('//img')
    iframelist = html.xpath('//iframe')
    imglist += iframelist
    # pool = Pool(5) # 添加线程池
    # pool = multiprocessing.Pool(5)
    # result = []
    for img in imglist:
        try:
            src = img.xpath("@src")[0]
        except Exception as e:
            continue
        if "http" not in src:
            img_url = parse.urljoin(prefix, src)
        else:
            img_url = src
        # result.append(pool.apply_async(func=down_img, args=(img_url,)))
        filename = down_img(img_url, prefix, path)
        if filename:
            article = re.sub(src, filename, article)  # 正则替换原来图片地址
        else:
            article = re.sub(src, '', article)  # 正则替换原来图片地址
    # 去掉不需要的标签
    result = remove_tags_with_content(article, which_ones=('script',))  # 删除script标签及内容
    result = remove_tags(result, which_ones=('a', 'font', 'div', 'tbody', 'script', 'form', 'frame', 'li', 'dd', 'dt', 'ul', 'iframe', 'ins'))  # 删除标签，不删除内容
    result = remove_comments(result, encoding='utf-8')
    # 使用demojize方法：用emoji短代码替换字符串中的unicode emoji,通过正则删除表情
    result = emoji.demojize(result)
    result = re.sub(':\S+?:', '', result)
    # content = modify_text(result)  #调用接口进行文章改写
    # if content:
    #     return content
    return result


# 下载图片
def down_img(url, referer, path):
    headers = {
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    try:
        sess = requests.Session()
        # sess.mount('http://', HTTPAdapter(max_retries=2))#增加重连次数
        # sess.mount('https://', HTTPAdapter(max_retries=2))
        sess.keep_alive = False  # 关闭多余连接
        response = requests.get(url=url, headers=headers, verify=False, timeout=30)
    except Exception as e:
        print(e)
        return None
    if response.status_code == 200:
        # houzui = url.split('.')[-1]
        # if len(houzui) > 5:
        #     houzui = 'jpg'
        # filename = timetimes() + '.' + houzui
        image_url_hash = hashlib.shake_256(response.url.encode()).hexdigest(5)
        image_perspective = re.sub(r'[\\/:*?"<>|]','',response.url.split('/')[-2]) # 正则替换掉符号
        image_filename = f'{image_url_hash}_{image_perspective}.jpg'
        if not os.path.exists(path):  # 判断路径是否存在，不存在则创建
            os.makedirs(path)
        with open(path + image_filename, 'wb') as f:
            f.write(response.content)
            f.close()
        # print(image_filename)
        return image_filename



# 生成13位时间戳
def timetimes():
    times = str(int(time.time() * 1000))
    return times


# 生成内容简介，取前60，没60取全部
def contenc_description(content):
    content = ''.join(content.split())
    if content:
        html = etree.HTML(content)
        # text = ''.join(html.xpath('//text()')).replace('\\n', '').replace('\n', '').replace('\\t', '').replace('\\r', '').replace('\t', '').replace('\r', '').replace(' ', '')
        text = ''.join(html.xpath('//text()'))
        text = re.sub('\s', ' ', text).replace(' ','')
        n = len(text)
        if n > 60:
            description = text[:60]
        else:
            description = text
        return description
    return None


# 利用分词统计出出现次数最多的标签
def get_words(content):
    content = ''.join(content.split())
    if content:
        html = etree.HTML(content)
        text = ''.join(html.xpath('//text()'))
        with open('D:/code/zimeiti/zimeiti/stop_words.txt', encoding='utf-8') as f:  # 读取停用词
            stop_words = f.read().split()
        ls = jieba.lcut(text)  # 分词
        # 去掉长度为1的词，包括标点
        newls = []
        for i in ls:
            if len(i) > 1:
                newls.append(i)
        # 统计词频
        ds = pd.Series(newls).value_counts()
        for i in stop_words:
            try:  # 处理找不到元素i时pop()方法可能出现的错误
                ds.pop(i)
            except:
                continue  # 没有i这个词，跳过本次，继续下一个词
        if len(ds) > 5:
            tag = ','.join(x.strip() for x in list(ds[:4].index) if x.strip() != '')
        else:
            tag = ','.join(x.strip() for x in list(ds.index) if x.strip() != '')
        return tag
    return None


# 连接数据库
def get_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='cc_11')  # db:表示数据库名称
    return conn


# 执行SQL语句
def execute(sql):
    conn = get_conn()
    cur = conn.cursor()
    try:
        result = cur.execute(sql)
        print(result)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def is_exists(data):
    conn = get_conn()
    cur = conn.cursor()
    sql = f"""select count(*) from cc_{data['name']} where url='{data['url']}'"""
    cur.execute(sql)
    results = cur.fetchall()
    # print(results)
    # print(type(results))  # 返回<class 'tuple'> tuple元组类型
    conn.commit()
    cur.close()
    conn.close()
    res = results[0][0]
    return res




def jquery_mock_callback():
    jQuery_Version = "3.6.0"
    return "jQuery" + (jQuery_Version + str(random.random())).replace(".", "") + "_" + str(int(round(time.time() * 1000)) - 1000)  # 版本号只留下数字，加上随机值与13位时间戳





