"""21经济网"""
import re
import time
import random
import scrapy
import os
from urllib.parse import urljoin, urlencode
import json
from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1, jquery_mock_callback


class MainSpider(scrapy.Spider):
    name = "21jingji"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.21jingji.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0

    def parse(self, response):
        lanmu1 = response.xpath('//div[@id="navList"]/a')
        lanmu2 = response.xpath('//div[@id="navList_df"]/a')
        lanmu3 = response.xpath('//div[@id="navWrap"]/a')[1:-1]
        lanmus = lanmu3
        print('栏目数量',len(lanmus))
        if lanmus:
            for lm in lanmus[1:]:
                ncolumn = lm.xpath('text()').get().strip()
                lmurl = urljoin('https://m.21jingji.com/', lm.xpath('@href').get())
                # print(lmurl)
                callback = jquery_mock_callback()
                for p in range(1, 200):
                    pamars = {
                        'callback': callback,
                        'page': 1,
                        'type': 'json',
                        '_': str(int(time.time() * 1000))
                    }
                    time.sleep(random.uniform(1.2, 2))
                    url = lmurl + '?' + urlencode(pamars)
                    print(ncolumn,url)
                    yield scrapy.Request(url=url, callback=self.lists,meta={'ncolumn': ncolumn})

    # def ejlanmu(self,response):
    #     lanmus = response.xpath('//div[@class="index-list-top"]/h3/a')
    #     if lanmus:
    #         for lm in lanmus:
    #             ncolumn = lm.xpath('text()').get().strip()
    #             lmurl = urljoin(response.url,lm.xpath('@href').get())
    #             # print(ncolumn,lmurl)
    #             time.sleep(random.uniform(1.2, 2.3))
    #             yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn})

    def lists(self, response):
        datas = re.findall(r'jQuery360.*?\((.*)\)', response.text)  # 取出数据
        print(datas)
        js_data = json.loads(datas[0])
        if js_data:
            for da in js_data:
                item = ZimeitiItem()
                item['url'] = da.get('url')
                print(item['url'])

                item['title'] = da.get('title')
                item['author'] = da.get('author')
                fmt_url = da.get('listthumb')

                item['description'] = da.get('description')
                # print(len(item['description']), item['description'])
                keywords = da.get('keywords')
                if keywords:
                    item['nkeywords'] = '#'.join(keywords.split(','))
                else:
                    item['nkeywords'] = None
                item['domian'] = self.name
                item['ncolumn'] = response.meta['ncolumn']
                item['naddtime'] = str(int(time.time()))
                num = is_exists({'name': self.name, 'url': item['url']})
                if num == 0:
                    if item['url']:
                        item['imgUrl'] = down_img(fmt_url, self.start_urls[0], self.path)
                        yield scrapy.Request(url=item['url'], callback=self.detail, meta={'item': item})
                else:
                    print('数据已存在')

    def detail(self, response):
        print('获取内容')
        self.s += 1
        item = response.meta['item']

        content = response.xpath('//div[@class="main_content"]').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text, response.url, self.path)
            if item['description'] is None or len(item['description']) == 0:
                item['description'] = contenc_description(item['Ncontent'])
            if item['nkeywords'] is None:
                item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item


if __name__ == '__main__':
    os.system('scrapy crawl 21jingji')
