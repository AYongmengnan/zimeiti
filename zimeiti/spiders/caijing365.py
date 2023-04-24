"""财经365"""
import re
import time

import scrapy
import os
from urllib.parse import urljoin
from lxml import etree
from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "caijing365"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://www.caijing365.com/"]
    path = f'D:/gushi365/images/{name}/'
    s = 0
    l = 0

    def parse(self, response, **kwargs):
        lanmus = response.xpath('//div[@class="menu2017 boxs"]/ul/li/a/@href').getall()
        if lanmus:
            for lan in lanmus[1:]:
                yield scrapy.Request(lan,callback=self.list1)

    def list1(self,response):
        lanmus = response.xpath('//div[@class="sonmenu2017"]/a')
        if lanmus:
            for lan in lanmus:
                typeurl = urljoin(self.start_urls[0], lan.xpath('@href').get())
                typename = lan.xpath('text()').get()
                yield scrapy.Request(url=typeurl, callback=self.list2, meta={'ncolumn': typename})

    def list2(self,response):
        lists = response.xpath('//ul[@class="news-con-list2017"]/li/a')
        if lists:
            for li in lists:
                fmt = li.xpath('div/img/@src').get()
                fmt_url = urljoin(self.start_urls[0], fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0], de_url)
                num = is_exists({'name': self.name, 'url': detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    imgUrl = down_img(fmt_url, response.url, self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=detail_url, callback=self.detail,
                                         meta={'ncolumn': response.meta['ncolumn'], 'imgUrl': imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = response.xpath('//ul[@class="pagelist"]/li/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(response.url, next_page)
            yield scrapy.Request(url=next_url, callback=self.list2, meta={'ncolumn': response.meta['ncolumn']})

    def detail(self,response):
        item = ZimeitiItem()
        item['title'] = response.xpath('//div[@class="container"]//h1/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@class="content-txt2017"]/*').getall()
        if content:
            text = "".join(content)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            item['Ncontent'] = refactoring_img(text, response.url, self.path)
            item['description'] = contenc_description(text)
            item['nkeywords'] = get_words(text)
            item['tag'] = '#'.join(response.xpath('//div[@class="label_tag"]/a/text()').getall())
            item['domian'] = 'caijing365'
            item['webName'] = '财经365'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl caijing365')