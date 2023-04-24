import re
import time

import requests
import json

import schedule
from scrapy import Selector

from zimeiti.public import refactoring_img, contenc_description, get_words, get_conn, execute

path = '//192.168.0.15/data/SEO/images/k8h8/'

session = requests.Session()

headers = {
    'authority': 'www.k8h8.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '__51vcke__JoX5b2bi347uSKwB=7aaf68b9-e05e-5987-b587-3eb9830c1fc4; __51vuft__JoX5b2bi347uSKwB=1682063686836; ripro_notice_cookie=1; PHPSESSID=q24he9d38vjd3o21rafs6vfm11; wordpress_logged_in_856380da3851d8f4589b6c868b64794e=mail_80793076|1683273320|CX7asfk9APXZ3O7KwgHxkAkUQUmDZnrYvYZI5ZfFzvZ|90798aa8dab5f660d7116e70e8aa9414dc39ef10b7b679b9c93c9181dcaf54e8; _tcnyl=1; __vtins__JoX5b2bi347uSKwB={"sid": "f707c35a-7758-58bf-a076-18247c6a66c3", "vd": 1, "stt": 0, "dr": 0, "expires": 1682326773138, "ct": 1682324973138}; __51uvsct__JoX5b2bi347uSKwB=5',
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

def article_content(info):
    item = {}
    print(info)
    id = info[0]
    item['ncolumn'] = info[1]
    item['url'] = info[2]
    item['imgUrl'] = info[4]
    response = session.post(url=item['url'],headers=headers)
    text = Selector(text=response.text)
    item['title'] = text.xpath('//div[@class="article-title"]/h1/text()|//h1[@class="entry-title"]/text()').get()
    y_content = text.xpath('//div[contains(@class,"entry-content")]/*').getall()[:-3]
    if y_content:
        item['Ncontent'] = refactoring_img(''.join(y_content),response.url,path)
        print(item['Ncontent'])
        item['description'] = contenc_description(item['Ncontent'])
        item['nkeywords'] = get_words(item['Ncontent'])
        item['tag'] = item['nkeywords']
    item['domian'] = 'k8h8'
    item['naddtime'] = str(int(time.time()))
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
    keys = ",".join(list(item.keys()))
    value_list = list(item.values())
    values = []
    for va in value_list:
        if va:
            if isinstance(va, list):
                va = ','.join(va)
            text = va.replace("'", "\\'").replace('"', '\\"')  # 单引号替换
            values.append(text)
        else:
            values.append('')
    value = "','".join(values)
    sql = f"""insert into cc_k8h8 ({keys}) VALUES ('{value}')"""
    if item['bdwp_url']:
        update_gather(id)
        return execute(sql)
    print('下载链接为空')
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
    # get_detail_url()
    schedule.every().day.at('10:00').do(get_detail_url)  # 每天10:30运行
    while True:
        schedule.run_pending()