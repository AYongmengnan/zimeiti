"""AI工具集导航"""
import hashlib
import os
import re
import time

import requests
import undetected_chromedriver as uc
import random
from urllib.parse import urljoin
from scrapy import Selector
from selenium.webdriver.common.by import By

from zimeiti.public import refactoring_img, contenc_description, get_words, execute, get_conn


def get_data():
    driver = uc.Chrome(version_main=111, use_subprocess=True)
    driver.maximize_window()
    driver.get('https://www.bing.com/')
    time.sleep(2)
    driver.get('https://ai-bot.cn/')
    time.sleep(6)
    source = driver.page_source
    response = Selector(text=source)
    lm_lists = response.xpath('//ul[@class="sub-menu"]/li/a')
    if lm_lists:
        for lm in lm_lists:
            lmname = lm.xpath('text()').get()
            lmurl = urljoin('https://ai-bot.cn/',lm.xpath('@href').get())
            time.sleep(0.5)
            get_lists(driver,lmname,lmurl)


def get_lists(driver,lmname,lmurl):
        driver.get(lmurl)
        source = driver.page_source
        response = Selector(text=source)
        de_lists = response.xpath('//div[@class="row"]/div/div/a|//div[contains(@class,"row")]/div/div/a')
        if de_lists:
            for de in de_lists:
                de_url = urljoin('https://ai-bot.cn/',de.xpath('@href').get())
                fmt = urljoin('https://ai-bot.cn/',de.xpath('div/div/img/@data-src').get())
                if 'ai-bot.cn' in de_url:
                    num = is_exists({'lm': lmname, 'url': de_url})
                    if num == 0:
                        savedata(de_url,driver,lmname,fmt)
                    else:
                        print('数据已存在')
    # if li == 'AI图像工具' or li == 'AI办公工具':
    #     lms = response.xpath('//div[@class="sidebar-menu-inner"]/ul/li/ul/li/a')
    #     for lm in lms:
    #         time.sleep(random.uniform(2.1,3.3))
    #         id = lm.xpath('@href').get().split('-')[-1]
    #         lanmu = lm.xpath('span/text()').get()
    #         url = f'https://ai-bot.cn/wp-admin/admin-ajax.php?id={id}&taxonomy=favorites&action=load_home_tab&post_id=0&sidebar=0'
    #         print(url)
    #         try:
    #             list_resp = Selector(text=requests.get(url).text)
    #         except Exception as e:
    #             print(e)
    #             return
    #         aixiezuo = list_resp.xpath('//a')
    #         if aixiezuo:
    #             savedata(aixiezuo,driver,lanmu)
    # else:
    #     aixiezuo = response.xpath(f'//div[contains(h4,"{li}")]/following-sibling::div[1]//a')
    # if aixiezuo:
    #     savedata(aixiezuo,driver,li)
    # driver.quit()
def savedata(de_url,driver,lmname,fmt):
    item = {}
    imgUrl = down_img(fmt, 'https://ai-bot.cn/', path)  # 调用下载图片方法
    time.sleep(random.uniform(2.4, 3.3))
    driver.get(de_url)
    time.sleep(4)
    text = Selector(text=driver.page_source)
    lms = text.xpath('//div[@class="site-body text-sm"]/a/text()').getall()
    num = is_exists({'lm': lmname, 'url': de_url})
    if num == 0:
        item['imgUrl'] = imgUrl
        l_img = urljoin('https://s0.wp.com/',text.xpath('//div[@class="siteico"]/img/@data-src').get())
        item['l_img'] = down_img(l_img, 'https://ai-bot.cn/', path)
        item['title2'] = text.xpath('//p[@class="mb-2"]/text()').get()
        item['title'] = text.xpath('//h1/text()').get()
        item['link'] = text.xpath('//span[@class="site-go-url"]/a/@href').get()
        s_url = text.xpath('//span[@class="site-go-url"]/following-sibling::a/@data-original-title').get()
        item['s_img'] = down_img(Selector(text=s_url).xpath('//img/@src').get(), de_url, path)
        item['like_count'] = text.xpath('//small[contains(@class,"like-count")]/text()').get()
        item['share_count'] = text.xpath('//small[contains(@class,"share-count")]/text()').get()
        item['tag'] = '#'.join(text.xpath('//span[@class="mr-2"]/a/text()').getall())
        content = text.xpath('//div[@class="panel site-content card transparent"]').getall()
        # print(content)
        if content:
            detail = "".join(content)
            item['Ncontent'] = refactoring_img(detail, de_url, path)
            if item['Ncontent']:
                item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])

            item['ncolumn'] = lms[-1]
            item['url'] = de_url
            item['seo_title'] = text.xpath('//title/text()').get()
            item['seo_keywords'] = text.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = text.xpath('//meta[@name="description"]/@content').get()

            keys = ",".join(list(item.keys()))
            value_list = list(item.values())
            values = []
            for va in value_list:
                if va:
                    if isinstance(va, list):
                        va = ','.join(va)
                    text = va.replace("'", "\\'").replace('"', '\\"')  # 引号替换
                    values.append(text)
                else:
                    values.append('')
            value = "','".join(values)
            sql = f"""insert into cc_ai_bot2 ({keys}) VALUES ('{value}')"""
            # print(sql)
            execute(sql)
    else:
        print('数据已存在。')
    # time.sleep(3)
    # driver.get(aixiezuo[1])
    # print(driver.page_source)
    # print(ai)

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
        image_perspective = re.sub(r'[\\/:*?"<>|]','',response.url.split('/')[-1]) # 正则替换掉符号
        image_filename = f'{image_url_hash}_{image_perspective}.jpg'
        if not os.path.exists(path):  # 判断路径是否存在，不存在则创建
            os.makedirs(path)
        with open(path + image_filename, 'wb') as f:
            f.write(response.content)
            f.close()
        # print(image_filename)
        return image_filename

def is_exists(data):
    conn = get_conn()
    cur = conn.cursor()
    sql = f"""select count(*) from cc_ai_bot2 where url='{data['url']}' and ncolumn='{data['lm']}'"""
    cur.execute(sql)
    results = cur.fetchall()
    # print(results)
    # print(type(results))  # 返回<class 'tuple'> tuple元组类型
    conn.commit()
    cur.close()
    conn.close()
    res = results[0][0]
    return res

if __name__ == '__main__':
    path = '//192.168.0.15/data/SEO/images/ai-bot2/'
    get_data()