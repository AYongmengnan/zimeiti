"""998时尚网"""
import re
import time
import random

import requests
import scrapy
import os
from urllib.parse import urljoin

from scrapy import Selector

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "ss998"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://www.ss998.com/health/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//div[@class="index_top3_menu"]/ul/li/a/@href').getall()[2:-1]
        if lanmus:
            for lm in lanmus:
                # ncolumn = lm.xpath('text()').get().strip()
                lmurl = urljoin(response.url,lm)
                yield scrapy.Request(url=lmurl,callback=self.ejlanmu)
    def ejlanmu(self,response):
        lanmus = response.xpath('//ul[@class="son-menu"]/li/a')
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('span/text()').get().strip()
                lmurl = urljoin(response.url,lm.xpath('@href').get())
                # print(ncolumn,lmurl)
                # time.sleep(random.uniform(1.2, 2.3))
                yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn})

    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="newslist"]/dl/dt/a[2]')
        if lists:
            for li in lists[:1]:
                # fmt = li.xpath('img/@src').get()
                # fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                if num == 0:
                    # imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    # print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn']})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@class="plist"]/ul/li/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//h1[@class="titleB"]/a/text()|//div[@class="title"]/h1/text()|//div[@id="headT"]/b/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        print(item['title'])
        descripte = response.xpath('//div[@class="content"]/p[contains(b,"导读")]/text()|//div[@class="mywords"]/p[contains(b,"导读")]/text()|//div[@id="text-con"]/p[contains(b,"导读")]/text()').get()
        if descripte:
            content = response.xpath('//div[@class="content"]/p|//div[@class="mywords"]/p|//div[@id="text-con"]/p').getall()[1:]
        else:
            content = response.xpath('//div[@class="content"]/p|//div[@class="mywords"]/p|//div[@id="text-con"]/p').getall()
        next_pages = response.xpath('//div[@class="mylist"]/ul/li/a/@href').getall()
        if next_pages:
            for page in next_pages[2:-1]:
                url = urljoin(response.url, page)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
                print(url)
                resp = requests.get(url=url, headers=headers)
                resp.encoding = resp.apparent_encoding
                html_text = Selector(text=resp.text)
                tx = html_text.xpath('//div[@class="content"]/p|//div[@class="mywords"]/p|//div[@id="text-con"]/p').getall()
                content += tx
        print(response.url,content)
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            if descripte:
                item['description'] = descripte
            else:
                item['description'] = contenc_description(item['Ncontent'])
            nkeywords = response.xpath('//div[@class="info"]/a/b/text()').getall()
            if nkeywords:
                item['nkeywords'] = '#'.join(nkeywords)
            else:
                item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '998时尚网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            # item['imgUrl'] = response.meta['imgUrl']
            # item['lmImgUrl'] = response.meta['lmImgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl ss998')