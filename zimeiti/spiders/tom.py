"""TOM网"""
import re
import time

import requests
import scrapy
import os
from urllib.parse import urljoin

from scrapy import Selector

from zimeiti.items import ZimeitiItem,ArchivesItem,ArctypeItem,ContentItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1,get_type
import urllib3
urllib3.disable_warnings()

class MainSpider(scrapy.Spider):
    name = "tom"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.tom.com/"]
    path = f'//192.168.0.15/data/SEO/images/ifensi/'
    # lm_types = get_type(name)
    def start_requests(self):
        for p in range(65,165):
            url = f'https://star.tom.com/json/show{p}.json?s=5600480' # p:1967
            print(url)
            yield scrapy.Request(url=url,callback=self.lists)
        # yield scrapy.Request(url='https://star.tom.com/json/show365.json?s=5600480', callback=self.lists)

    def lists(self,response):
        data = response.json()
        for k,v in data.items():
            fmt_lists = v[2]
            if fmt_lists:
                imgUrl = down_img(urljoin(self.start_urls[0],fmt_lists[0]),self.start_urls[0],self.path)
            else:
                imgUrl = None
            de_url = urljoin(self.start_urls[0],v[3])
            # print(de_url)
            num = is_exists({'name': 'ifensi', 'url': de_url})
            if num == 0:
                yield scrapy.Request(url=de_url, callback=self.detail, meta={'imgUrl':imgUrl})
            else:
                print('数据库已存在')
                pass

    def detail(self,response):
        print('获取内容')
        item = ZimeitiItem()
        title = response.xpath('//div[@class="content_news_box"]/h1/text()').get()
        if title:
            title = title.strip()
        item['title'] = title
        text = response.xpath('//div[@class="news_box_text"]').getall()
        if text:
            text = "".join(text)
            # content = refactoring_img(text,response.url,self.path)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = 'ifensi'
            # item['webName'] = 'TOM网'
            item['imgUrl'] = response.meta['imgUrl']
            item['url'] = response.url
            item['ncolumn'] = '星闻聚焦'
            item['naddtime'] = str(int(time.time()))
            item['author'] = response.xpath('//meta[@name="author"]/@content').get()
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item
            # print(item)





if __name__ == '__main__':
    os.system('scrapy crawl tom')