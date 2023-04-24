"""小熊下载站"""
import json
import re
import time
import random

import requests
import scrapy
import os
from urllib.parse import urljoin

from zimeiti.items import ZimeitiItem
from zimeiti.public import refactoring_img, down_img, contenc_description, get_words, timetimes, execute, is_exists, \
    refactoring_img1
import math

class MainSpider(scrapy.Spider):
    name = "bear20"
    # allowed_domains = ["xxx.com"]
    start_urls = ["https://www.bear20.com/"]
    path = f'//192.168.0.15/data/SEO/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = response.xpath('//div[@class="nav"]/div/ul/li/a')[1:]
        if lanmus:
            for lmu in lanmus:
                # ncolumn = lmu.xpath('text()').get().strip()
                lmurl = urljoin(response.url, lmu.xpath('@href').get())
                # print(ncolumn,lmurl)
                yield scrapy.Request(url=lmurl,callback=self.ejlm)

    def ejlm(self,response):
        lists = response.xpath('//div[@class="classification floatL"]/dl')[1:]
        lanmus = []
        if lists:
            for li in lists:
                ejlm = li.xpath('dd/a')
                if ejlm:
                    lanmus += ejlm
                else:
                    lanmus.append(li.xpath('dt/a'))
        if lanmus:
            for lmu in lanmus:
                ncolumn = lmu.xpath('text()').get().strip()
                # lmurl = urljoin(response.url, lmu.xpath('@href').get())
                x_url = lmu.xpath('@href').get().split('.')[0]
                lmurl = f'https://www.bear20.com{x_url}_pv_total_1.json?_={int(time.time() * 1000)}'
                # print(ncolumn,lmurl)
                yield scrapy.Request(url=lmurl,callback=self.lists,meta={'ncolumn':ncolumn,'x_url':x_url})

    def lists(self,repsonse):
        text = repsonse.text
        if '出错了' in text:
            pass
        else:
            json_data = json.loads(text)
            data_list = json_data['list']
            for da_li in data_list:
                item = ZimeitiItem()
                item['description'] = da_li['digest']
                item['title'] = da_li['name']
                item['seo_title'] = da_li['seoDigest']
                item['seo_keywords'] = da_li['seoKeyword']
                item['seo_description'] = da_li['shortName']
                item['url'] = da_li['url']
                item['imgUrl'] = down_img(urljoin(self.start_urls[0],da_li['image5']),repsonse.url,self.path)
                item['left_img'] = down_img(urljoin(self.start_urls[0],da_li['logoLarge']),repsonse.url,self.path)
                item['ncolumn'] = repsonse.meta['ncolumn']
                num = is_exists({'name': self.name, 'url': item['url']})
                if num == 0:
                    yield scrapy.Request(url=item['url'],callback=self.detail,meta={'dict':item})
            totalSize = json_data['totalSize']
            pages = math.ceil(int(totalSize)/20)
            if pages>1:
                for p in range(2,pages+1):
                    lmurl = f'https://www.bear20.com{repsonse.meta["x_url"]}_pv_total_{p}.json?_={int(time.time() * 1000)}'
                    yield scrapy.Request(url=lmurl,callback=self.lists1,meta={'ncolumn':repsonse.meta['ncolumn']})

    def lists1(self,repsonse):
        text = repsonse.text
        if '出错了' in text:
            print('出错了')
            pass
        else:
            json_data = json.loads(text)
            data_list = json_data['list']
            for da_li in data_list:
                item = ZimeitiItem()
                item['description'] = da_li['digest']
                item['title'] = da_li['name']
                item['seo_title'] = da_li['seoDigest']
                item['seo_keywords'] = da_li['seoKeyword']
                item['seo_description'] = da_li['shortName']
                item['url'] = da_li['url']
                item['imgUrl'] = down_img(urljoin(self.start_urls[0],da_li['image5']),repsonse.url,self.path)
                item['left_img'] = down_img(urljoin(self.start_urls[0],da_li['logoLarge']),repsonse.url,self.path)
                item['ncolumn'] = repsonse.meta['ncolumn']
                num = is_exists({'name': self.name, 'url': item['url']})
                if num == 0:
                    yield scrapy.Request(url=item['url'], callback=self.detail, meta={'dict': item})

    def detail(self,response):
        item = response.meta['dict']
        print('获取内容')
        item['version'] = response.xpath('//div[@class="softwarename"]/span/text()').get()
        onlink = response.xpath('//div[@class="downLoad"]/button[@class="ptgj down"]/@onclick|//div[@class="downLoad"]/button[@class="down"]/@onclick|//button[contains(.,"顶部立即下载")]/@onclick').get()
        xid = re.findall(r"downLink\('(.*?)'\)",onlink)
        item['down_url'] = None
        item['likes'] = None
        if xid:
            item['down_url'] = 'https://downapi.bear20.com/down/s/hp' + xid[0] + '_10,4,0'
            item['likes'] = self.get_likes(xid[0])
        item['bd_down_url'] = response.xpath('//div[@class="downLoad"]/a[@class="ptgj down Topdown bdwp new"]/@href|//button[contains(.,"顶部百度网盘下载")]/@href').get()
        titleList = response.xpath('//div[@class="titleList"]/ul/li')
        if titleList:
            item['size'] = titleList[0].xpath('span/text()').get()
            item['downs'] = titleList[1].xpath('span/text()').get()
            # item['language'] = titleList[2]
            item['language'] = titleList[2].xpath('span/text()').get()
            item['t_system'] = ''.join(titleList[3].xpath('span/text()').get().strip().replace('\\n','').replace('\\t','').replace('\\r','').split())
            item['up_date'] = titleList[5].xpath('span/text()').get()
        item['t_type'] = response.xpath('//div[@class="titleList"]/ul/li/a/span/text()').get()
        content = response.xpath('//div[@class="content"]').getall()
        if content:
            text = "".join(content)
            if '<!-- 历史版本 -->' in text:
                text = text.split('<!-- 历史版本 -->')[0]
            else:
                text = text.split('<div id="lsbb"')[0]
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = item['nkeywords']
            item['domian'] = self.name
            item['webName'] = '小熊下载站'
            item['naddtime'] = str(int(time.time()))
            item['seo_title'] = response.xpath('//title/text()').get()
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item


    def get_likes(self,xid):
        print('获取点赞数')
        url = f'https://nodeinterface.yesky.com/getSoftLike.do?sId={xid}'
        try:
            response = requests.get(url).json()
            print(response)
        except Exception as e:
            print(e)
            return None
        return str(response['count'])


if __name__ == '__main__':
    os.system('scrapy crawl bear20')