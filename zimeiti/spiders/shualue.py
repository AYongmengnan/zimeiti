"""说说网"""
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
    name = "shualue"
    # allowed_domains = ["xxx.com"]
    # start_urls = ["http://www.ibagua.com.cn/"]
    path = f'//192.168.0.15/data/SEO/images/51tietu/'
    s = 0
    l = 0
    # def parse(self, response):
    #     lanmus = response.xpath('//div[@class="header"]/ul/li/a')[:4]
    #     if lanmus:
    #         for lm in lanmus:
    #             ncolumn = lm.xpath('text()').get().strip()
    #             lmurl = urljoin(response.url,lm.xpath('@href').get())
    #             yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn})
    # def ejlanmu(self,response):
    #     lanmus = response.xpath('//div[@class="index-list-top"]/h3/a')
    #     if lanmus:
    #         for lm in lanmus:
    #             ncolumn = lm.xpath('text()').get().strip()
    #             lmurl = urljoin(response.url,lm.xpath('@href').get())
    #             # print(ncolumn,lmurl)
    #             time.sleep(random.uniform(1.2, 2.3))
    #             yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn})
    def start_requests(self):
        url = 'https://www.shualue.com/juzidaquan/'
        yield scrapy.Request(url=url,callback=self.lists)

    def lists(self,repsonse):
        lists = repsonse.xpath('//ul[@class="g-gxlist-article"]/li/a')
        if lists:
            for li in lists:
                # fmt = li.xpath('img/@src').get()
                # fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(repsonse.url,de_url)
                num = is_exists({'name':'51tietu','url':detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    # imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    # print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail)
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@class="tsp_nav"]/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists)

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//h1/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@id="zoom"]//td/*[not(name()="a")]').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = response.xpath('//div[@class="m-daodu"]/text()').get()
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = '#'.join(response.xpath('//div[@id="zoom"]//td/a/text()').getall())
            item['domian'] = '51tietu'
            item['webName'] = '说说网'
            item['url'] = response.url
            item['ncolumn'] = '句子'
            item['naddtime'] = str(int(time.time()))
            # item['imgUrl'] = response.meta['imgUrl']
            # item['lmImgUrl'] = response.meta['lmImgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl shualue')