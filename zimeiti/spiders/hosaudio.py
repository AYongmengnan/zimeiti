"""一点排行"""

import time

import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "hosaudio"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://hosaudio.com"]
    path = 'D:/gushi365/images/hosaudio/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//div[@class="subnav"]/ul/li/a')
        # lanmu2 = response.xpath('//div[@class="subnav"]/ul/li/a')
        # lanmus = lanmu1+lanmu2
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('@title').get()
                # print(ncolumn)
                lanmu_url = self.start_urls[0] + lm.xpath('@href').get()
                yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn})
    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="asan"]/ul/li/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
                fmt_url = urljoin(self.start_urls[0],fmt)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                if num == 0:
                    imgUrl = down_img(fmt_url, repsonse.url,self.path)  # 调用下载图片方法
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn'],'imgUrl':imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@class="page"]/li/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        title = response.xpath('//div[@class="newsnr"]/h1/text()').get()
        if title:
            item['title'] = title
        content = response.xpath('//div[@class="newsnr"]/div[last()]/*').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = 'hosaudio'
            item['webName'] = '一点排行'
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
        #         if va:
        #             text = va.replace("'", "\\'") # 单引号替换
        #             values.append(text)
        #         else:
        #             values.append(va)
        #     value = "','".join(values)
        #     sql = f"""insert into cc_{self.name} ({keys}) VALUES ('{value}')"""
        #     execute(sql)
        #     self.l +=1
        # print(f'内容数量{self.s},储存数量{self.l}')




if __name__ == '__main__':
    os.system('scrapy crawl hosaudio')