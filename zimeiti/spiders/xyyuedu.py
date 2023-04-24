"""轩宇阅读网"""
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
    name = "xyyuedu"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.xyyuedu.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//div[@class="nav"]/ul/li/a')[1:]
        if lanmus:
            for lm in lanmus:
                # lmt = urljoin(self.start_urls[0],lm.xpath('img/@src').get())
                # lmImgUrl = down_img(lmt, response.url, self.path)  # 调用下载图片方法
                lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                # print(lanmu_url)
                yield scrapy.Request(url=lanmu_url,callback=self.ejlanmu)
    def ejlanmu(self,response):
        lanmus = response.xpath('//div[@class="index-list-top"]/h3/a')
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('text()').get().strip()
                lmurl = urljoin(response.url,lm.xpath('@href').get())
                # print(ncolumn,lmurl)
                time.sleep(random.uniform(1.2, 2.3))
                yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn})

    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="list-main"]/ul/li/a/@href').getall()
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
                    time.sleep(random.uniform(1.2,2.3))
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn']})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@class="list-pages"]/ul/li/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//div[@class="article-title"]/h1/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@class="article-article"]').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = '#'.join(response.xpath('//div[@class="relatedTags"]/a/text()').getall())
            item['domian'] = self.name
            item['webName'] = '轩宇阅读网'
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
    os.system('scrapy crawl xyyuedu')