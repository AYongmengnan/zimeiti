"""搜鲜网"""
import re
import time

import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "sosoxian"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.sosoxian.com/"]
    path = f'D:/gushi365/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//ul[@class="Nav"]/li/div/h3/a')
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('@title').get().strip()
                # print(ncolumn)
                lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                # print(lanmu_url)
                yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn})
    def lists(self,repsonse):
        lists = repsonse.xpath('//li[@class="zww"]/div/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
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
        next_page = repsonse.xpath('//ul[@class="pagelist"]/li/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        title = response.xpath('//span[@class="title"]/text()').get()
        if title:
            item['title'] = title
        content = response.xpath('//div[@class="bodys"]/*').getall()
        if content:
            text = "".join(content)
            item['Ncontent'],item['image_urls'] = refactoring_img1(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = response.xpath('//meta[@name="description"]/@content').get()
            item['nkeywords'] = '#'.join(response.xpath('//meta[@name="keywords"]/@content').get().split(','))
            item['tag'] = '#'.join(response.xpath('//div[@class="tBwrc"]/a/text()').getall())
            item['domian'] = self.name
            item['webName'] = '搜鲜网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
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
    os.system('scrapy crawl sosoxian')