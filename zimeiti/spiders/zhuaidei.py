"""拽得网"""
import re
import time

import scrapy
import os
from urllib.parse import urljoin
import requests
from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1
from lxml import etree
import chardet
import html

class MainSpider(scrapy.Spider):
    name = "zhuaidei"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://www.zhuaidei.com/"]
    path = f'D:/gushi365/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//div[@class="container"]/nav/ul/li/a')[1:-1]
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('text()').get().strip()
                # print(ncolumn)
                lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                # print(lanmu_url)
                yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn})
    def lists(self,repsonse):
        item = ZimeitiItem()
        item['ncolumn'] = repsonse.meta['ncolumn']
        lists = repsonse.xpath('//ul[@class="mr-item news-list"]/li/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
                fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                if num == 0:
                    item['imgUrl'] = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    print(item['imgUrl'])
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'item':item})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@class="pages"]/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        item = response.meta['item']
        detail_urls = response.xpath('//div[@class="pages"]/a/@href').getall()
        text = []
        if detail_urls:
            for de_u in detail_urls[1:-1]:
                str_list = []
                url = urljoin(response.url,de_u)
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
                resp = requests.get(url=url,headers=headers)
                resp.encoding = resp.apparent_encoding
                html_text = etree.HTML(resp.text)
                tx = html_text.xpath('//div[@class="articleContent"]/*')
                for t in tx:
                    ps = html.unescape((etree.tostring(t)).decode('utf-8'))
                    str_list.append(ps)
                text += str_list
        else:
            text = response.xpath('//div[@class="articleContent"]/*').getall()
        if text:
            text = "".join(text)
            title = response.xpath('//div[@class="articleDetail"]/h1/text()').get()
            if title:
                item['title'] = title.strip()
            item['Ncontent'] = refactoring_img(text, response.url, self.path)
            item['image_urls'] = None
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = response.xpath('//p[@class="articleIntro"]/text()').get()
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '拽得网'
            item['url'] = response.url
            item['naddtime'] = str(int(time.time()))
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            # print(item)
            yield item








        # if de_urls:
        #     for li in list(set(de_urls[1:])):
        #         str_list = []
        #         headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        #         resp = requests.get(url=li,headers=headers)
        #         resp.encoding = resp.apparent_encoding
        #         html_text = etree.HTML(resp.text)
        #         tx = html_text.xpath('//div[@class="articleContent"]/*')
        #         for t in tx:
        #             ps = html.unescape((etree.tostring(t)).decode('utf-8'))
        #             str_list.append(ps)
        #         text += str_list





if __name__ == '__main__':
    os.system('scrapy crawl zhuaidei')