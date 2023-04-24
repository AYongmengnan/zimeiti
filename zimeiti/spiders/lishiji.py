"""历史记"""
import re
import time

import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "lishiji"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.lishiji.cn/"]
    path = f'//192.168.0.15/data/SEO/images/misanguo/'
    s = 0
    l = 0
    def start_requests(self):
        for p in range(90):
            url = f'https://www.lishiji.cn/lishi/86/p{p}/'
            yield scrapy.Request(url=url,callback=self.lists)
    def lists(self,repsonse):
        lists = repsonse.xpath('//div[contains(@class,"listbox1")]/div[@class="boxL"]/a|//div[contains(@class,"listbox1")]/div[@class="pic4"]/a[1]')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
                fmt_url = urljoin(self.start_urls[0],fmt)
                # # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':'misanguo','url':detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn': '群雄逐鹿'})
                else:
                    print('数据库已存在')
                    pass
        # next_page = repsonse.xpath('//div[@class="pagination"]/a[contains(text(),"下一页")]/@href').get()
        # if next_page:
        #     next_url = urljoin(repsonse.url,next_page)
        #     yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//div[@class="newsbox01"]/h1/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@id="newscont"]').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = "#".join(response.xpath('//div[@class="timer"]/a/text()').getall())
            item['domian'] = 'misanguo'
            item['webName'] = '迷三国'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            # item['imgUrl'] = response.meta['imgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl lishiji')