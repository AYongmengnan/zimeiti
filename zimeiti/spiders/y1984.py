"""历史网_古今历史网_上下五千年历史"""
import random
import time

import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    get_typyid, put_data, refactoring_img1


class MainSpider(scrapy.Spider):
    name = "y1984"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://www.y1984.com/index.html"]
    path = f'D:/gushi365/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//div[@class="container"]/ul/li/a')[1:]
        if lanmus:
            for lm in lanmus:
                # ncolumn = lm.xpath('text()').get().strip()
                lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                print(len(lanmu_url))
                yield scrapy.Request(url=lanmu_url,callback=self.parse_lanmu)
    def parse_lanmu(self,response):
        lanmus = response.xpath('//div[@class="zimulu"]/ul/li/a')[1:]
        if lanmus:
            for lm in lanmus:
                ncolumn2 = lm.xpath('text()').get().strip()
                lanmu_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn2})
    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="hotimg"]/div/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
                fmt_url = urljoin(self.start_urls[0],fmt)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                if num == 0:
                    imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn'],'imgUrl':imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//ul[@class="pagination"]/li/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        title = response.xpath('//div[@class="viewtitle"]/h1/text()').get().strip()
        if title:
            item['title'] = title
        content = response.xpath('//div[@id="contentText"]/*').getall()
        if content:
            text = "".join(content)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            item['Ncontent'], item['image_urls'] = refactoring_img1(text, response.url, self.path)
            item['description'] = contenc_description(text)
            item['nkeywords'] = get_words(text)
            item['tag'] = item['nkeywords']
            item['domian'] = 'y1984'
            item['webName'] = '历史网_古今历史网_上下五千年历史'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
            yield item
        # #组装插入sql语句
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
        #     yield item
        # print(f'内容数量{self.s},储存数量{self.l}')
        # typename = response.meta['ncolumn2']
        # typeid = get_typyid(typename)
        # if title and content and typeid:
        #     text = "".join(content)
        #     data = {'title': title,
        #             'typeid': typeid,
        #             'channel': '1',
        #             '__post_password': "xiangzi",
        #             'content': refactoring_img(text, response.url, self.path),
        #             'add_time': int(time.time()),
        #             'arcrank': 0,
        #             'click': random.randint(100, 10000),
        #             'tags': 'fghd,你好'
        #             }
        #     print(data)
        #     put_data(data)




if __name__ == '__main__':
    os.system('scrapy crawl y1984')