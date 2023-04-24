"""FACE妆点网"""
import re
import time

import requests
import scrapy
import os
from urllib.parse import urljoin

from scrapy import Selector

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "zdface"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://zdface.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//div[@class="wraper"]/ul/li/a/@href').getall()[1:]
        if lanmus:
            for lm in lanmus:
                yield scrapy.Request(url=lm,callback=self.ejlanmu)
    def ejlanmu(self,response):
        lanmus = response.xpath('//div[@class="fl"]/a')[1:]
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('text()').get().strip()
                lmurl = urljoin(response.url,lm.xpath('@href').get())
                # print(ncolumn,lmurl)
                yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn})

    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="ContList"]/ul/li/i[@class="iTit"]/a/@href').getall()
        if lists:
            for li in lists:
                # fmt = li.xpath('img/@src').get()
                # fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                # de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],li)
                num = is_exists({'name':self.name,'url':detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    # imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    # print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn']})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@class="pagelist"]/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//div[@class="wraper"]//h1/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@id="txt"]').getall()
        detail_urls = response.xpath('//div[@class="pagelist"]/a/@href').getall()
        if detail_urls:
            for de_u in detail_urls[:-2]:
                url = urljoin(response.url, de_u)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
                print(url)
                resp = requests.get(url=url, headers=headers)
                resp.encoding = resp.apparent_encoding
                html_text = Selector(text=resp.text)
                tx = html_text.xpath('//div[@id="txt"]').getall()
                content += tx
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = response.xpath('//p[@id="desc"]/text()').get()
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = 'FACE妆点网'
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
    os.system('scrapy crawl zdface')