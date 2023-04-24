"""历史网"""
import re
import time

import scrapy
import os
from urllib.parse import urljoin
from lxml import etree
from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "lishi"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.lishi.net/laozhaopian"]
    path = f'D:/gushi365/images/{name}/'
    s = 0
    l = 0
    """老照片"""
    def parse(self, response, **kwargs):
        lists = response.xpath('//a[@class="item-thumb"]')
        if lists:
            for lis in lists:
                url = urljoin(self.start_urls[0],lis.xpath('@href').get())
                imgurl = urljoin(self.start_urls[0],lis.xpath('img/@src').get())
                num = is_exists({'name': self.name, 'url': url})
                if num == 0:
                    imgUrl = down_img(imgurl,response.url,self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=url,callback=self.detail,meta={'imgUrl':imgUrl})
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            next_url = urljoin(response.url, next_page)
            yield scrapy.Request(url=next_url, callback=self.parse)
    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        title = response.xpath('//h1[@class="entry-title"]/text()').get()
        if title:
            item['title'] = title
        content = response.xpath('//div[@class="entry-content"]/p').getall()
        if content:
            text = "".join(content)
            item['Ncontent'],item['image_urls'] = refactoring_img1(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = response.xpath('//meta[@name="description"]/@content').get()
            if item['description'] is None:
                item['description'] = contenc_description(text)
            item['nkeywords'] = get_words(text)
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '历史网'
            item['url'] = response.url
            item['ncolumn'] = '老照片'
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
            yield item
    """各栏目"""
    # def start_requests(self):
    #     url = 'https://www.lishi.net/wp-admin/admin-ajax.php'
    #     lanmu = {'先秦秦汉历史': '160', '魏晋南北朝': '161', '隋唐元明清': '162', '民国历史': '163', '现代史': '164', '亚洲历史': '121', '美洲历史': '126', '欧洲历史': '124', '非洲历史': '137', '大洋洲及南极洲历史': '140', '中国人物': '141', '世界人物': '142', '神话人物': '143', '影视剧人物': '144', '焦点事件': '120', '中国事件': '157', '外国事件': '158', '历史解秘': '147', '野史趣闻': '5', '战争': '155', '传统文化': '148', '西方文化': '149', '神话故事': '151', '历史典故': '150', '文史百科': '180', '世界地理': '153', '中国地理': '152'}
    #     for k,v in lanmu.items():
    #         for p in range(1,100):
    #             form_data = {
    #                 'action': 'wpcom_load_posts',
    #                 'page': f'{p}',
    #                 'taxonomy': 'category',
    #                 'id': f'{v}',
    #                 'type': 'default',
    #                 'attr': '',
    #                 'order': ''}
    #             yield scrapy.FormRequest(url=url,formdata=form_data,callback=self.parse,meta={'ncolumn':k})
    #
    # def parse(self, response, **kwargs):
    #     print(response.text)
    #     if response.text == '0' or response.status != 200:
    #         pass
    #     else:
    #         html = etree.HTML(response.text)
    #         url_lis = html.xpath('//a[@class="item-img-inner"]/@href')
    #         if url_lis:
    #             for u in url_lis:
    #                 yield scrapy.Request(u,callback=self.detail,meta={'ncolumn':response.meta['ncolumn']})
    #
    # def detail(self,response):
    #     item = ZimeitiItem()
    #     title = response.xpath('//h1[@class="entry-title"]/text()').get()
    #     if title:
    #         item['title'] = title.strip()
    #     content = response.xpath('//div[@class="entry-content"]/*').getall()
    #     if content:
    #         text = "".join(content)
    #         # item['Ncontent'] = refactoring_img(text,response.url,self.path)
    #         item['Ncontent'], item['image_urls'] = refactoring_img1(text, response.url, self.path)
    #         item['description'] = contenc_description(text)
    #         item['nkeywords'] = get_words(text)
    #         item['tag'] = item['nkeywords']
    #         item['domian'] = 'lishi'
    #         item['webName'] = '历史网'
    #         item['url'] = response.url
    #         item['ncolumn'] = response.meta['ncolumn']
    #         item['naddtime'] = str(int(time.time()))
    #         item['imgUrl'] = None
    #         yield item






if __name__ == '__main__':
    os.system('scrapy crawl lishi')