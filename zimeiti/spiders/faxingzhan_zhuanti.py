"""发型站_专题"""
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
    name = "faxingzhan"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.faxingzhan.com/special/index.html"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s_url = 'https://www.faxingzhan.com/'
    def parse(self, response):
        lmurls = response.xpath('//div[@class="menu-content"]/ul/li/a')
        if lmurls:
            for lmu in lmurls:
                ncolumn = lmu.xpath('text()').get().strip()
                lmurl = urljoin(response.url, lmu.xpath('@href').get())
                # print(ncolumn,lmurl)
                yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn})

    def lists(self,repsonse):
        lists = repsonse.xpath('//ul[@id="noteid"]/li/a')
        if lists:
            for li in lists:
                # fmt = li.xpath('img/@src').get()
                # fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                if num == 0:
                    # imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    # print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn'],'imgUrl':None})
                else:
                    print('数据库已存在')
                    pass
        # next_page = repsonse.xpath('//div[@class="pages"]/a[contains(text(),"下一页")]/@href').get()
        # if next_page:
        #     next_url = urljoin(repsonse.url,next_page)
        #     yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        item = ZimeitiItem()
        item['title'] = response.xpath('//div[@class="title"]/h1/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@class="content"]').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = response.xpath('//div[@class="guide"]/p/text()|//div[@class="describe"]/p/text()').get()
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '发型站'
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
    os.system('scrapy crawl faxingzhan')