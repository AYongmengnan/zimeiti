"""工作总结范文 - 壹壹范文网
"""
import re
import time

import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "11gw"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://11gw.com/list/gzzjfw"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lms = []
        lanmus = response.xpath('//ul[@id="menu-justnews-menu"]/li')[1:]
        if lanmus:
            for lan in lanmus:
                ejlm = lan.xpath('ul/li/a')
                if ejlm:
                    lms += ejlm
                else:
                    lms.append(lan.xpath('a'))
        if lms:
            for lm in lms:
                ncolumn = lm.xpath('text()').get().strip()
                lmurl = urljoin(response.url, lm.xpath('@href').get())
                # print(ncolumn,lmurl)
                yield scrapy.Request(url=lmurl, callback=self.lists, meta={'ncolumn': ncolumn})

    def lists(self,repsonse):
        # print(repsonse.url)
        lists = repsonse.xpath('//ul[contains(@class,"post-loop")]/li[@class="item"]/div[@class="item-img"]/a[@class="item-img-inner"]')
        # print(len(lists))
        if lists:
            for li in lists:
                fmt = li.xpath('img/@data-original').get()
                fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn'],'imgUrl':imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        item = ZimeitiItem()
        title = response.xpath('//div[@class="entry-head"]/h1/text()').get()
        if title:
            item['title'] = title
        content = response.xpath('//div[@class="entry-content"]/*[not(name()="div")]').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '壹壹范文网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item
        #组装插入sql语句
        # if item['title'] and item['Ncontent']:
        #     keys = ",".join(list(item.keys()))
        #     value_list = list(item.values())
        #     values = []
        #     for va in value_list:
        #         print(va)
        #         if va:
        #             text = va.replace("'", "\\'")  # 单引号替换
        #             values.append(text)
        #         else:
        #             values.append('')
        #     value = "','".join(values)
        #     sql = f"""insert into cc_{self.name} ({keys}) VALUES ('{value}')"""
        #     execute(sql)
        #     self.l +=1
        # print(f'内容数量{self.s},储存数量{self.l}')
        # print(item['img_replace'])
        # for img_re in item['img_replace']:
        #     item['Ncontent'] = re.sub(list(img_re.keys())[0], list(img_re.values())[0], item['Ncontent']) #正则替换原来图片地址





if __name__ == '__main__':
    os.system('scrapy crawl 11gw')