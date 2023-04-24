# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES settings
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import re
import time
from urllib import parse

import pymysql
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
# from scrapy import log

# 保存数据
class ZimeitiPipeline:

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='cc_11',charset="utf8mb4",autocommit=True)  # db:表示数据库名称
        self.cur = self.conn.cursor()
    # def process_item(self, item, spider):
    #     if item.__class__ == BaseItem:
    #     # savexxx
    #     else item.__class__ == BookItem:
    #     # savexxx222
    #     return item

    def process_item(self,item,spider):
        # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='cc_11')  # db:表示数据库名称
        # cur = conn.cursor()
        # if 'image_urls' in item:
        #     item.pop('image_urls')
        if item['title'] and item['Ncontent']:
        # if item['url']:
            keys = ",".join(list(item.keys()))
            value_list = list(item.values())
            values = []
            for va in value_list:
                if va:
                    if isinstance(va,list):
                        va = ','.join(va)
                    text = va.replace("'", "\\'").replace('"', '\\"')  # 单双引号替换
                    values.append(text)
                else:
                    values.append('')
            value = "','".join(values)
            sql = f"""insert into cc_{item['domian']} ({keys}) VALUES ('{value}')"""
            # print(sql)
            self.conn.ping(reconnect=True)  # 如果连接断开重新连接
            result = self.cur.execute(sql)
            if result == 1:
                print('数据保存成功')
            else:
                print('数据保存失败')
            self.conn.commit()
            # self.cur.close()
            # self.conn.close()
            return item
    def __del__(self):
        self.cur.close()
        self.conn.close()
# 图片下载
class ImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'referer': '',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    def get_media_requests(self, item, info):
        if item['image_urls']:
            print(item['image_urls'])
            for image_url in item['image_urls']:
                self.default_headers['referer'] = item['url']
                image_url = parse.urljoin(item['url'],image_url)
                yield Request(image_url, headers=self.default_headers)
        else:
            return item

    def item_completed(self, results, item, info):
        if results:
            image_paths = [x['path'] for ok, x in results if ok]
            image_urls = [x['url'] for ok, x in results if ok]
            # print(results)
            img_yuan = item['image_urls']
            if not image_paths:
                # raise DropItem("Item contains no images")
                # item['Ncontent'] = None  # 请求出现错误或失败不保存数据
                return item
            for i in range(len(image_urls)):
                for img_y in img_yuan:
                    if img_y in image_urls[i]:
                        # print(img_y,image_urls[i])
                        item['Ncontent'] = re.sub(img_y, image_paths[i].split('/')[-1], item['Ncontent'])  # 正则替换原来图片地址
                        continue
            item['effective'] = '1'
            return item
            # item['image_paths'] = image_paths
            # item.pop('image_urls')
            # item.pop('image_paths')
        return item

    def file_path(self, request, response=None, info=None, *, item=None): # 自定义文件名
        image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        image_perspective = request.url.split('/')[-2]
        image_filename = f'{image_url_hash}_{image_perspective}.jpg'
        # image_filename = f'{int(time.time() * 1000)}.jpg'
        return item['domian'] + '/' + image_filename