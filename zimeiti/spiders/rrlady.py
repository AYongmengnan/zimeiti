"""魅力女人网"""
import re
import time

import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "rrlady"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://www.rrlady.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmu1 = response.xpath('//ul[@id="menu-navigation"]/li/ul/li/a')
        lanmu2 = response.xpath('//ul[@id="menu-navigation"]/li/a')[5:]
        lanmus = lanmu1+lanmu2
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('text()').get().strip()
                # print(ncolumn)
                lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                # print(lanmu_url)
                yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn})
    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="posts-gallery-img"]/a|//div[@class="like-post-box"]/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
                if fmt:
                    fmt_url = urljoin(self.start_urls[0],fmt)
                else:
                    fmt_url = re.findall(r'\((.*?)\)',li.xpath('div[@class="image"]/@style').get())[0]
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn']})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//ul[@class="pages"]/li/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//header[@class="post_header"]/h1/text()|//div[@class="post-title"]/h1/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@class="content_post"]|//div[@class="post-content"]').getall()
        # print(response.url,content)
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            description = response.xpath('//div[@class="juntext"]/text()').get()
            if description:
                description = description.strip().split('导读：')[-1]
            else:
                description = response.xpath('//div[@class="detail"]/text()').get()
            item['description'] = description
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '魅力女人网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            # item['imgUrl'] = response.meta['imgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl rrlady')