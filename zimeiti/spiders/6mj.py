"""中国民间故事网"""
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
    name = "6mj"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.6mj.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    # lm_types = get_type(name)
    def parse(self, response):
        lanmu1 = response.xpath('//ul[@class="nav-menu pull-left"]/li/div/ul/li/a')
        lanmu2 = response.xpath('//nav[@id="main-navigation"]/ul/li/ul/li/a')
        lanmus = lanmu1 + lanmu2
        # print(len(lanmus))
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('text()').get().strip()
                lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                # print(ncolumn)
                # print(lanmu_url)
                yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn})
    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="meta"]/table/tr//a/@href').getall()
        if lists:
            for li in lists:
                # fmt = li.xpath('img/@src').get()
                # fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                # de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],li)
                print(detail_url)
                num = is_exists({'name':self.name,'url':detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    # imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    # print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn']})
                else:
                    print('数据库已存在')
                    pass
        page_list = repsonse.xpath('//div[@class="meta"]/div/a/@href').getall()
        if page_list:
            for pl in page_list:
                next_url = urljoin(repsonse.url,pl)
                yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        item = ZimeitiItem()
        title = response.xpath('//div[contains(@class,"row-fluid content")]/div/h1/font/b/text()|//title/text()').get()
        if title:
            title = title.strip()
        item['title'] = title
        text = response.xpath('//div[@class="meta"]/p').getall()[2:]
        detail_urls = response.xpath('//div[@id="page"]/ul/li/a/@href').getall()
        if detail_urls:
            for de_u in detail_urls[1:-2]:
                url = urljoin(response.url, de_u)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
                print(url)
                resp = requests.get(url=url, headers=headers,verify=False)
                resp.encoding = resp.apparent_encoding
                html_text = Selector(text=resp.text)
                tx = html_text.xpath('//div[@class="meta"]/p').getall()[2:]
                text += tx
        if text:
            text = "".join(text)
            # content = refactoring_img(text,response.url,self.path)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '中国民间故事网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['author'] = response.xpath('//meta[@name="author"]/@content').get()
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item
            # print(item)





if __name__ == '__main__':
    os.system('scrapy crawl 6mj')