"""风景园林网"""
import re
import time
import random
import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1


class MainSpider(scrapy.Spider):
    name = "chla"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://chla.com.cn/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//ul[contains(@class,"navbar-nav")]/li/a/@href').getall()[1:2]
        if lanmus:
            for lmu in lanmus:
                lmurl = urljoin(response.url, lmu)
                # print(ncolumn,lmurl)
                yield scrapy.Request(url=lmurl,callback=self.erjilm)
    def erjilm(self, response):
        lmurls = response.xpath('//div[contains(@class,"classify-list")]//a[contains(text(),"查看更多")]/@href').getall()
        lmnames = response.xpath('//ul[@id="classify-nav"]/li/text()').getall()
        # lanmus = dict(zip(lmnames,lmurls))
        # print(lmurls)
        # print(lmnames)
        if lmurls:
            for i in range(len(lmnames)):
                lmurl = urljoin(response.url, lmurls[i])
                print(lmurl)
                # print(ncolumn,lmurl)
                yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':lmnames[i]})

    def lists(self,repsonse):
        lists = repsonse.xpath('//div[@class="one-c_grid"]/a|//div[@class="mar_10"]//div[@class="classify-img"]/a')
        if lists:
            for li in lists:
                fmt = li.xpath('img/@src|div/img/@src').get()
                fmt_url = urljoin(self.start_urls[0],fmt)
                # print(fmt_url)
                de_url = li.xpath('@href').get()
                if 'weixin.qq' in de_url:
                    print(de_url)
                    detail_url = de_url.split('url=')[-1]
                else:
                    detail_url = urljoin(self.start_urls[0],de_url)
                num = is_exists({'name':self.name,'url':detail_url})
                # yield scrapy.Request(url='http://www.41sky.com/gprj/2018-10-24/110.html', callback=self.detail, meta={'ncolumn': repsonse.meta['ncolumn']})
                if num == 0:
                    imgUrl = down_img(fmt_url,repsonse.url,self.path)  # 调用下载图片方法
                    print(imgUrl)
                    time.sleep(random.uniform(1.3,1.8))
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn'],'imgUrl':imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@id="pages"]/a[contains(text(),"下一页")]/@href').get()
        if next_page:
                page = re.findall(r'.*/(.*?)\.html', next_page)
                if page and page[0] != '1':
                    next_url = urljoin(self.start_urls[0],next_page)
                    yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        item['title'] = response.xpath('//div[@class="article-box"]/h1/text()|//h1[@id="activity-name"]/text()').get()
        if item['title']:
            item['title'] = item['title'].strip()
        content = response.xpath('//div[@id="endtext"]|//div[@id="js_content"]').getall()
        print(content)
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '风景园林网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
            # item['lmImgUrl'] = response.meta['lmImgUrl']
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item






if __name__ == '__main__':
    os.system('scrapy crawl chla')