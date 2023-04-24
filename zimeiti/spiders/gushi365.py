"""故事365"""
import html
import re
import time
from lxml import etree

import requests
import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "gushi365"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.gushi365.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0

    def parse(self, response):
        lanmu = response.xpath('//nav[@id="site-nav"]/div/ul/li')
        lanmu_list = []
        if lanmu:
            for lm in lanmu[1:-1]:
                ej = lm.xpath('ul/li/a')
                if ej:
                    if isinstance(ej, list):
                        lanmu_list += ej
                    else:
                        lanmu_list.append(ej)
                else:
                    lanmu_list.append(lm.xpath('a'))
        for lms in lanmu_list:
            ncolumn = lms.xpath('text()|span/text()').get().strip()
            # print(ncolumn)
            lanmu_url = urljoin(self.start_urls[0], lms.xpath('@href').get())
            # print(lanmu_url)
            yield scrapy.Request(url=lanmu_url, callback=self.lists, meta={'ncolumn': ncolumn})

    def lists(self, repsonse):
        lists = repsonse.xpath('//main[@id="main"]/article/figure/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src').get()
                fmt_url = urljoin(self.start_urls[0], fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                detail_url = urljoin(self.start_urls[0], de_url)
                num = is_exists({'name': self.name, 'url': detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    imgUrl = down_img(fmt_url, repsonse.url, self.path)  # 调用下载图片方法
                    print(imgUrl)
                    yield scrapy.Request(url=detail_url, callback=self.detail,
                                         meta={'ncolumn': repsonse.meta['ncolumn'], 'imgUrl': imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url, next_page)
            yield scrapy.Request(url=next_url, callback=self.lists, meta={'ncolumn': repsonse.meta['ncolumn']})

    def detail(self, response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        wei = response.xpath('//div[@class="page-links"]/a[contains(text(),"尾页")]/@href').get()
        text = response.xpath('//div[@class="single-content"]/div[1]/following-sibling::*[not(name()="h2")]').getall()
        if wei:
            w_url = urljoin(response.url, wei)
            page = re.findall(r'_(.*?)\.html', w_url)
            if page:
                for p in range(2,int(page[0])+1):
                    str_list = []
                    d_url = re.sub(r'_(.*?)\.html', f'_{p}.html', w_url)
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
                    resp = requests.get(url=d_url, headers=headers)
                    resp.encoding = resp.apparent_encoding
                    html_text = etree.HTML(resp.text)
                    tx = html_text.xpath('//div[@class="single-content"]/div[1]/following-sibling::*[not(name()="h2")]')
                    for t in tx:
                        ps = html.unescape((etree.tostring(t)).decode('utf-8'))
                        str_list.append(ps)
                    text += str_list
        # content = response.xpath('//div[@class="single-content"]/p').getall()
        if text:
            text = "".join(text)
            item['Ncontent'] = refactoring_img(text, response.url, self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            title = response.xpath('//h1[@class="entry-title"]/text()').get()
            if title:
                item['title'] = title.strip()
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '故事365'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item


if __name__ == '__main__':
    os.system('scrapy crawl gushi365')
