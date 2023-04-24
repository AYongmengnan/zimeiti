"""娱乐广播网"""
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
    name = "yulefm"
    # allowed_domains = ["xxx.com"]
    start_urls = ["http://www.yulefm.com/"]
    path = f'D:/gushi365/images/{name}/'
    s = 0
    l = 0
    def parse(self, response):
        lanmus = {
            '内地明星娱乐新闻': 'http://www.yulefm.com/sneidi/', '海外明星娱乐新闻': 'http://www.yulefm.com/shaiwai/', '华语明星娱乐新闻': 'http://www.yulefm.com/sgangtai/',#明星娱乐资讯
            '内地电影娱乐新闻':'http://www.yulefm.com/dneidi/','华语电影娱乐新闻':'http://www.yulefm.com/dgangtai/','海外电影娱乐新闻':'http://www.yulefm.com/dhaiwai/','预告片资讯':'http://www.yulefm.com/dyugaopian/','麻辣点评资讯':'http://www.yulefm.com/ddianping/',#电影娱乐资讯
            '内地娱乐':'http://www.yulefm.com/vfilm/','华语娱乐':'http://www.yulefm.com/vnews/','海外娱乐':'http://www.yulefm.com/vbig/',#电视娱乐资讯
            '内地音乐娱乐新闻':'http://www.yulefm.com/yneidi/','海外音乐娱乐资讯':'http://www.yulefm.com/yhaiwai/','华语音乐娱乐资讯':'http://www.yulefm.com/ygangtai/','MV音乐娱乐资讯':'http://www.yulefm.com/mv/','MP3音乐娱乐资讯':'http://www.yulefm.com/mp3/',#音乐娱乐资讯
            '新闻':'http://www.yulefm.com/tu/xw/',#图片娱乐资讯
            '时尚':'http://www.yulefm.com/shishang/',#时尚
            '综合新闻':'http://www.yulefm.com/xzns/',#综合新闻
            '滚动新闻':'http://www.yulefm.com/news/',#滚动新闻
            '明星专题':'http://www.yulefm.com/zt/',#明星专题
            '女性':'http://www.yulefm.com/nvren/',#女性
            '原创':'http://www.yulefm.com/ent/',#原创
            '星闻':'http://sh.yulefm.com/xingwen/',#上海站
            '电影':'http://ln.yulefm.com/dianying/'#辽宁站
        }
        keji =  {'科技快讯':'http://www.yulefm.com/tech/kuaixun/','通信':'http://www.yulefm.com/tech/telecom/','IT':'http://www.yulefm.com/tech/it/','智能':'http://www.yulefm.com/tech/smart/','移动互联':'http://www.yulefm.com/tech/internet/','手机':'http://www.yulefm.com/tech/mobile/','数码':'http://www.yulefm.com/tech/digi/','5G':'http://www.yulefm.com/tech/5g/'},#科技
        for k,v in lanmus.items():
            yield scrapy.Request(url=v,callback=self.lists,meta={'ncolumn':k})

    def lists(self,repsonse):
        print(repsonse.text)
        lists = repsonse.xpath('//div[@id="list-row"]/div/div/a')
        print(lists)
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
                    time.sleep(random.uniform(1.2,2.5))
                    yield scrapy.Request(url=detail_url,callback=self.detail,meta={'ncolumn':repsonse.meta['ncolumn'],'imgUrl':imgUrl})
                else:
                    print('数据库已存在')
                    pass
        next_page = repsonse.xpath('//div[@id="list-pager"]/a[contains(text(),"下一页")]/@href').get()
        if next_page:
            next_url = urljoin(repsonse.url,next_page)
            yield scrapy.Request(url=next_url,callback=self.lists,meta={'ncolumn':repsonse.meta['ncolumn']})

    def detail(self,response):
        print('获取内容')
        self.s += 1
        item = ZimeitiItem()
        title = response.xpath('//div[@id="content-title"]/h1/text()').get()
        if title:
            item['title'] = title
        content = response.xpath('//div[@id="content-body"]/table').getall()
        if content:
            text = "".join(content)
            item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = refactoring_img(text,response.url,self.path)
            # item['Ncontent'] = content
            item['description'] = contenc_description(item['Ncontent'])
            item['nkeywords'] = get_words(item['Ncontent'])
            item['tag'] = '#'.join(response.xpath('//div[@id="content-tags"]/ul/li/a/text()').getall())
            item['domian'] = self.name
            item['webName'] = '娱乐广播网'
            item['url'] = response.url
            item['ncolumn'] = response.meta['ncolumn']
            item['naddtime'] = str(int(time.time()))
            item['imgUrl'] = response.meta['imgUrl']
            item['origin'] = '娱乐广播网'
            item['seo_keywords'] = response.xpath('//meta[@name="keywords"]/@content').get()
            item['seo_description'] = response.xpath('//meta[@name="description"]/@content').get()
            yield item





if __name__ == '__main__':
    os.system('scrapy crawl yulefm')