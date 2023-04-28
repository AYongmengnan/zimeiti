# -*- coding:utf-8 -*-
"""
公用方法：
下载文章中的图片内容
获取关键字、标签、简介
入库前判断数据是否存在
"""
import hashlib
import json
import os
import random
import re
import time

import emoji
import redis
import pymysql
import requests
from urllib import parse
from urllib.parse import quote
from multiprocessing import Pool
import multiprocessing
import urllib3
from lxml.html import tostring
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
        # image_url_hash = hashlib.shake_256(response.url.encode()).hexdigest(5)
        image_url_hash = hashlib.shake_256(response.url.encode()).hexdigest(10)
        image_perspective = re.sub(r'[\\/:*?"<>|]','',response.url.split('/')[-2]) # 正则替换掉符号
        image_filename = f'{image_url_hash}_{image_perspective}.jpg'
        if not os.path.exists(path):  # 判断路径是否存在，不存在则创建
            os.makedirs(path)
        with open(path + image_filename, 'wb') as f:
            f.write(response.content)
            f.close()
        # print(image_filename)
        return image_filename

# 文章改写
def modify_text(content):
    url = 'https://apis.5118.com/wyc/rewrite'
    payload = {
        'txt': quote(content),  # 全文内容(长度不能超过5000字符(含html字符),如含有html字符,使用quote进行编码)
        'retype': 1,  # retype=1:模型3号(默认选中);retype=2:模型2号;retype=3:模型1号
        'keephtml': True,  # 是否保留html格式(默认true:保留,false:去除html格式)
        'sim': 1,  # 是否返回相似度(默认0不开启,1为开启)
        # 'strict':1  #严选换词(可以选择不同档位进行严选换词,档位越高换词越严格,默认为0:关闭状态)
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': '04C013511EB34E6299C11E56837CC152'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    if response['errcode'] == '0':
        return response['data']
    else:
        print('返回错误代码：',response['errcode'])
        return None


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


#获取栏目id
def get_typyid(typename):
    url = 'http://192.168.0.167:10101/api/publishArticle/getType?__post_flag&pwd=eyoucms'
    response = requests.get(url)
    typenames = json.loads(response.text)
    print(typenames)
    # typeid = typenames.get(typename)
    # return typeid


# 通过接口上传数据
def put_data(data):
    url = 'http://192.168.0.167:10101/api/publishArticle/insertArchives?__post_flag=post'
    response = requests.post(url=url, data=data)
    result = json.loads(response.text)
    if result.get('msg'):
        print('数据插入成功')
    else:
        print(result)


def redis_con():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='root', db=0,
                                decode_responses=True)  # 本地
    r = redis.Redis(connection_pool=pool)
    return r


"""测试取出所有图片图片"""


def refactoring_img1(article, prefix, path):
    images_list = []
    if not article:
        return article, []
    html = etree.HTML(article)
    imglist = html.xpath('//img')
    # iframelist = html.xpath('//iframe')
    # imglist += iframelist
    for img in imglist:
        try:
            src = img.xpath("@src")[0]
            images_list.append(src)
        except Exception as e:
            continue
    #     if "http" not in src:
    #         img_url = parse.urljoin(prefix, src)
    #     else:
    #         img_url = src
    #     # result.append(pool.apply_async(func=down_img, args=(img_url,)))
    #     filename = down_img(img_url,prefix,path)
    #     if filename:
    #         article = re.sub(src, filename, article) #正则替换原来图片地址

    # 去掉不需要的标签
    result = remove_tags(article, which_ones=(
    'a', 'table', 'tr', 'td', 'font', 'div', 'tbody', 'script', 'form', 'frame', 'li', 'dd', 'dt', 'ul', 'iframe'))
    # 删除HTML中的注释
    result = remove_comments(result, encoding='utf-8')
    # 使用demojize方法：用emoji短代码替换字符串中的unicode emoji,通过正则删除表情
    result = emoji.demojize(result)
    result = re.sub(':\S+?:', '', result)
    return result, images_list


# 连接服务器数据
def server_con(name):
    conn = pymysql.connect(host='47.97.152.141', port=3306, user='apt10_com', passwd='PEsPnytkCNddbjHb', db=name)  # db:表示数据库名称
    return conn

# 获取栏目信息
def get_type(name):
    conn = server_con(name)
    cur = conn.cursor()
    sql = f"""select id,typename from ey_arctype"""
    cur.execute(sql)
    results = cur.fetchall()
    key = []
    value = []
    for res in results:
        key.append(res[1])
        value.append(res[0])
    return dict(zip(key,value))


# 服务器执行SQL语句
def execute1(name,sql):
    conn = server_con(name)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        return False


# 获取插入后的aid
def get_server_dataid(name,title):
    con = server_con(name)
    cur = con.cursor()
    sql = f"""select aid from ey_archives where title='{title}'"""
    cur.execute(sql)
    aid = cur.fetchall()[0][0]
    con.commit()
    cur.close()
    con.close()
    return aid  # int

def chat_(name,sql):
    con = server_con(name)
    cur = con.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    con.commit()
    cur.close()
    con.close()


def jquery_mock_callback():
    jQuery_Version = "3.6.0"
    return "jQuery" + (jQuery_Version + str(random.random())).replace(".", "") + "_" + str(int(round(time.time() * 1000)) - 1000)  # 版本号只留下数字，加上随机值与13位时间戳



if __name__ == '__main__':
    # article = """<div class="article-content"><img src="http://p3.p2statp.com/large/pgc-image/15325353401729e0c10e769.jpg"><p class="pgc-img-caption"></p><img src="http://p9.p2statp.com/large/pgc-image/15325353404110aae03a2e7.jpg"><p class="pgc-img-caption"></p><p>————————</p><p>欢迎关注“元浦说文”头条号</p><p>金元浦 教授中国人民大学文化创意产业研究所所长</p><p>中外文艺理论学会副会长教育部文化部动漫类教材专家委员会副主任中国人民大学文学院教授、博导中国传媒大学、上海交通大学博导</p><p>“元浦说文”由中国人民大学金元浦教授创办。目标在于速递文化信息、传播深度思考、汇集文化创意产业的业界和学术精英，搭建产学研的合作桥梁。</p></div>"""
    # url = 'https://hosaudio.com/archives/62706.html'
    # path = 'D:/gushi365/images/'
    # # print(refactoring_img(article,url,path))
    # # print(contenc_description(article))
    # # timetimes()
    # is_exists({'name':'hosaudio','url':'http://hosaudio.com/archives/65041.html'})
    # get_typyid()
    # get_typyid('')
    # print(get_type('6mj'))
    # sql = """insert into cc_all (title,Ncontent) VALUES ('1234465','werqfwfgerg')"""
    # execute(sql)
    # print(get_server_dataid('6mj','苹果 A17 续写性能新神话！安卓阵营集体被甩开了'))
    content = """<p>许多宠主都是有苦恼，自己家的小狗太蠢了不太好，太蠢了也不太好。绝大多数宠主都喜爱聪明的狗狗，他们如同一个小朋友一样，主人家可以和他们有共多的互动交流。</p><p>可是小狗一旦聪慧到一定水平，主人家也会很烦恼的。小狗自身是十分开朗的小动物，如同一个小机灵鬼，尽管不容易张口讲话，可是他们能用自身的行動告知宠主，他们究竟想做什么。</p><p>如今大部分宠主全是工薪族，平常沒有非常的時间守候自个的宠狗。像哈士奇这类顽皮的小狗，主人家都需要把他们关到铁笼里才会安心，由于他们会撕家。</p><p style="text-align:center"><img src="0318150438383671.png" title="大金毛开门拿外卖送餐，外卖员哈哈大笑，汪：是吃的来了吗" alt="大金毛开门拿外卖送餐，外卖员哈哈大笑，汪：是吃的来了吗" width="580" height="543"></p><p>可是没多久以后宠主们便会发觉，自己家的狗子学好开门锁了，无论是铁笼上的，或是门边的。自然要开门那一定就需要是小狗了，像金毛、哈士奇、阿拉斯加这种。</p><p>金毛是小狗中十分聪慧的一个种类了，这并不，一位网民家中就养了一只大金毛，叫乐乐，乐乐十分聪慧，也十分温和聪明，关键的是，乐乐便是那只能开门的狗。</p><p style="text-align:center"><img src="0318150438383674.jpeg" alt="大金毛开门拿外卖送餐，外卖员哈哈大笑，汪：是吃的来了吗" title="大金毛开门拿外卖送餐，外卖员哈哈大笑，汪：是吃的来了吗" width="580" height="540"></p><p>前几日乐乐主人家点了一份外卖送餐，未过一会儿送快餐的小伙就按了电子门铃，外卖员原本认为消费者来开门了，想不到门开启以后，从门后边外伸一只狗脑壳。</p><p>哈哈，原来是乐乐将门打开了，难道说是嗅到了送餐的香气了没有，见到一脸希望的大金毛，外卖员也是笑出了鼻涕泡，看见金毛这一目光就仿佛在说：是吃的来了吗？</p><p style="text-align:center"><img src="0318150438383677.jpeg" alt="大金毛开门拿外卖送餐，外卖员哈哈大笑，汪：是吃的来了吗" title="大金毛开门拿外卖送餐，外卖员哈哈大笑，汪：是吃的来了吗" width="580" height="558"></p><p>这年代连狗都是会开门拿外卖送餐了，见到金毛自身梦见门坏了，宠主也是有一些焦虑不安，这金毛还行，这如果二哈学会了自身开门那还得了，网民说的没错，二哈如果会开门，重要情况下不可通敌吗？</p><p>可是不得不承认的是，假如自己家的小狗会开门了，宠主们或是要多留意一点的，万一小狗悄悄跑出去伤到他人，或是吓住他人那么就不好了。</p><p>小狗聪慧的确会让业主很意外惊喜，可是也会很烦恼的，狗子学习培训开门的过程中很简单，可是他们学会了，就需要防着他们了，并不是那麼找邦企的。</p>"""

    print(modify_text(content))

