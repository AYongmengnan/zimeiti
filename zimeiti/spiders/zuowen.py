"""作文网"""
import re
import time

import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "zuowen"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://www.zuowen.com/gushi/"]
    path = f'//192.168.0.15/data/SEO/images/6mj/'
    s = 0
    l = 0
    def parse(self, response):
        # lanmus = response.xpath('//ul[@class="gs_menu"]/li/a')[:2]
        # if lanmus:
        #     for lm in lanmus:
        #         ncolumn = lm.xpath('h2/text()').get().strip()
        #         # print(ncolumn)
        #         lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
        #         # print(lanmu_url)
        #         yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn})
        yield scrapy.Request(url='http://www.zuowen.com/gushi/yizhigushi/',callback=self.lists,meta={'ncolumn':'机智故事'})
    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="artbox_l_t"]/a/@href').getall()
        if lists:
            for li in lists:
                # fmt = li.xpath('img/@src').get()
                # fmt_url = urljoin(self.start_urls[0],fmt)
                # # print(fmt_url)
                # de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],li)
                num = is_exists({'name':'6mj','url':detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    # imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    # print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn']})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@class="artpage"]/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//h1[@class="h_title"]/text()').get()
        print(item['title'])
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@class="con_content"]/p').getall()[:-5]
        print(content)
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = '6mj'
            # item['webName'] = '作文网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            # item['imgUrl'] = response.meta['imgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl zuowen')