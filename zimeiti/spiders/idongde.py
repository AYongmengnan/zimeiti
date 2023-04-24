"""懂得"""
import json
import re
import time

import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "idongde"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.idongde.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response,**kwargs):
        lanmu1 = response.xpath('//div[@class="header_left"]/ul/li/a')[1:]
        lanmu2 = response.xpath('//div[@class="more_nav"]/ul/li/a')
        lanmus = lanmu1 + lanmu2
        if lanmus:
            for lm in lanmus:
                ncolumn = lm.xpath('text()').get().strip()
                # print(ncolumn)
                lm_url = urljoin(self.start_urls[0],lm.xpath('@href').get())
                # print(lanmu_url)
                uid = re.findall(r'category/(.*?)\.shtml',lm_url)[0]
                # print(uid)
                for p in range(1,51):
                    lanmu_url = f'https://www.idongde.com/category/{uid}/page?page={p}&size=18'
                    yield scrapy.Request(url=lanmu_url,callback=self.lists,meta={'ncolumn':ncolumn})
    def lists(self,repsonse):
        datas = json.loads(repsonse.text)
        lists = datas['data']['data']
        for li in lists:
            alias = li['alias']
            cover = li['cover']
            tags = li['tags']
            tag = []
            for t in tags:
                tag.append(t['name'])
            tag = "#".join(tag)
            de_url = f'https://www.idongde.com/c/{alias}.shtml'
            num = is_exists({'name': self.name, 'url': de_url})
            if num == 0:
                imgUrl = down_img(cover,repsonse.url,self.path)  # 调用下载图片方法
                print(imgUrl)
                yield scrapy.Request(url=de_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn'],'tag':tag,'imgUrl':imgUrl})
        # lists = repsonse.xpath('//div[@class="list_51"]/a/@href').getall()
        # if lists:
        #     for li in lists:
        #         # fmt = li.xpath('img/@src').get()
        #         # fmt_url = urljoin(self.start_urls[0],fmt)
        #         # # print(fmt_url)
        #         # de_url = li.xpath('@href').get()
        #         detail_url = urljoin(self.start_urls[0],li)
        #         num = is_exists({'name':self.name,'url':detail_url})
        #         # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
        #         if num == 0:
        #             # imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
        #             # print(imgUrl)
        #             yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn']})
        #         else:
        #             print('数据库已存在')
        #             pass
        # next_page = repsonse.xpath('//div[@class="pagination"]/a[contains(text(),"下一页")]/@href').get()
        # if next_page:
        #     next_url = urljoin(repsonse.url,next_page)
        #     yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//div[@class="nav-con"]/h1/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@class="article-content"]').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '懂得'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            # item['imgUrl'] = response.meta['imgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl idongde')