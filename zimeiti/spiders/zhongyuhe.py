"""宠物资讯网"""
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
    name = "zhongyuhe"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://zhongyuhe.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lm_lists = response.xpath('//ul[@class="nav navbar-nav wpcom-adv-menu"]/li')[:-1]
        lanmus = []
        if lm_lists:
            for lm_li in lm_lists:
                ejlms = lm_li.xpath('ul/li/a')
                if ejlms:
                    lanmus += ejlms
                else:
                    lanmus.append(lm_li.xpath('a'))
        if lanmus:
            for lmu in lanmus:
                ncolumn = lmu.xpath('text()').get().strip()
                lmurl = urljoin(response.url, lmu.xpath('@href').get())
                # print(ncolumn,lmurl)
                time.sleep(random.uniform(1.5,2.2))
                yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn})

    def lists(self,repsonse):
        lists = repsonse.xpath('//ul[contains(@class,"post-loop")]/li/div/a[@class="item-img-inner"]')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
                fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                if num == 0:
                    imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    print(imgUrl)
                    time.sleep(random.uniform(1.5,2.2))
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn'],'imgUrl':imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            time.sleep(random.uniform(1.5,2.2))
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[contains(@class,"entry-content ")]').getall()
        if content:
            text = "".join(content)
            text = text.split('<div class="pagination')[0]
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '宠物资讯网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
            # item['lmImgUrl'] = response.meta['lmImgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl zhongyuhe')