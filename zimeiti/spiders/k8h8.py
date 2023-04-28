"""
千云网
采集所有文章地址
"""
import re
import time
import random
import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "k8h82"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.k8h8.com/"]
    path = f'C:/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//ul[@id="menu-menu-1"]/li/a/@href').getall()[1:4]
        if lanmus:
            for lm in lanmus:
                yield scrapy.Request(url=lm,callback=self.erji)
    def erji(self,response):
        time.sleep(random.uniform(1.2,1.8))
        lanmus = response.xpath('//div[@class="filters"]/ul[2]/li/a')
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('text()').get().strip()
                lm_url = urljoin(response.url,lm.xpath('@href').get())
                print(ncolumn,lm_url)
                time.sleep(random.uniform(1.4, 2.7))
                yield scrapy.Request(url=lm_url,callback=self.lists,meta={'ncolumn':ncolumn})

    def lists(self,repsonse):

        item = ZimeitiItem()
        lists = repsonse.xpath('//div[@class="placeholder"]/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@data-src').get()
                fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                imgUrl = down_img(fmt_url, repsonse.url, self.path)  # 调用下载图片方法
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0], de_url)
                item['ncolumn'] = repsonse.meta['ncolumn']
                item['domian'] = 'k8h82'
                item['url'] = detail_url
                item['imgUrl'] = imgUrl
                yield item

        next_page = repsonse.xpath('//div[contains(@class,"pagination")]/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            time.sleep(random.uniform(1.4, 2.7))
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})





if __name__ == '__main__':
    os.system('scrapy crawl k8h82')