"""星闻热点"""
import json
import re
import time
from scrapy import Selector
import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "ifensi"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://www.ifensi.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//ul[@class="nav"]/li/a')[1:]
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('text()').get().strip()
                # print(ncolumn)
                lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                # print(lanmu_url)
                yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn})
    def lists(self,response):
        tagid = response.xpath('//a[@class="more"]/@data-tagidmd5').get()
        if tagid:
            for p in range(1,99):
                url = f'http://www.ifensi.com/index.php?m=api&c=Ajax&a=arcpagelist&lang=cn&page={p}&pagesize=5&tagid=list001&tagidmd5={tagid}'
                data = {
                    '_ajax': '1'
                }
                yield scrapy.FormRequest(url=url,formdata=data,callback=self.detail_list,meta={'ncolumn':response.meta['ncolumn']})

    def detail_list(self,response):
        data = json.loads(response.text)
        lastpage = data['data']['lastpage']
        if lastpage == 0:
            pass
        msg = data['data']['msg']
        text = Selector(text=msg)
        lists = text.xpath('//li/a')
        if lists:
            for li in lists:
                fmt_url = urljoin('http://www.ifensi.com/',li.xpath('img/@src').get())
                detail_url = urljoin('http://www.ifensi.com/',li.xpath('@href').get())
                print(fmt_url,detail_url)
                num = is_exists({'name': self.name, 'url': detail_url})
                if num == 0:
                    imgUrl = down_img(fmt_url,response.url,self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':response.meta['ncolumn']})


    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//h1[@class="article-title"]/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@class="article-box"]').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '星闻热点'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            # item['imgUrl'] = response.meta['imgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl ifensi')