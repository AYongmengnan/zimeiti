"""快乐故事网"""
import html
import re
import time

import requests
import scrapy
import os
from urllib.parse import urljoin
from scrapy import Selector
from lxml import etree

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "kuailegushi"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://kuailegushi.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    text_list = []
    def parse(self, response):
        lanmu = response.xpath('//ul[@id="menu-main"]/li')[1:]
        lanmu_list = []
        if lanmu:
            for lm in lanmu:
                ej = lm.xpath('ul/li/a')
                if ej:
                    if isinstance(ej, list):
                        lanmu_list += ej
                    else:
                        lanmu_list.append(ej)
                else:
                    lanmu_list.append(lm.xpath('a'))
        for lms in lanmu_list:
            ncolumn = lms.xpath('text()').get().strip()
            # print(ncolumn,len(ncolumn))
            lanmu_url = urljoin(self.start_urls[0], lms.xpath('@href').get())
            # print(lanmu_url)
            yield scrapy.Request(url=lanmu_url, callback=self.lists, meta={'ncolumn': ncolumn})
    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@id="post_list_box"]/article/figure/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
                fmt_url = urljoin(self.start_urls[0], fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0], de_url)
                num = is_exists({'name': self.name, 'url': detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    imgUrl = down_img(fmt_url, repsonse.url, self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=detail_url, callback=self.detail,
                                         meta={'ncolumn': repsonse.meta['ncolumn'], 'imgUrl': imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@class="nav-links"]/span[@class="next"]/a/@href|//a[contains(@title,"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        item = ZimeitiItem()
        title = response.xpath('//h1[@class="entry-title"]/text()').get()
        if title:
            item['title'] = title
        text = response.xpath('//div[@class="single-content"]/*').getall()
        # detail_urls = response.xpath('//div[@id="page"]/ul/li/a/@href').getall()
        # if detail_urls:
        #     for de_u in detail_urls[2:-1]:
        #         url = urljoin(response.url, de_u)
        #         headers = {
        #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        #         print(url)
        #         resp = requests.get(url=url, headers=headers)
        #         resp.encoding = resp.apparent_encoding
        #         html_text = Selector(text=resp.text)
        #         tx = html_text.xpath('//div[@id="ny"]/*').getall()
        #         text += tx
        if text:
            text = "".join(text)
            item['Ncontent'] = refactoring_img(text, response.url, self.path)
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['author'] = response.xpath('//meta[@name="author"]/@content').get()
            item['domian'] = self.name
            item['webName'] = '快乐故事网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            # print(item)
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl kuailegushi')