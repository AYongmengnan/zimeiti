# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZimeitiItem(scrapy.Item):
    # define the fields for your item here like:
    ncolumn = scrapy.Field()
    ncolumn1 = scrapy.Field()
    ncolumn2 = scrapy.Field()
    title = scrapy.Field()
    Ncontent = scrapy.Field()
    naddtime = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    nkeywords = scrapy.Field()
    tag = scrapy.Field()
    author = scrapy.Field()
    domian = scrapy.Field()
    webName = scrapy.Field()
    isUpdata = scrapy.Field()
    reContent = scrapy.Field()
    localUrl = scrapy.Field()
    imgUrl = scrapy.Field()
    lmImgUrl = scrapy.Field()

    path = scrapy.Field()
    img_replace = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

    seo_title = scrapy.Field()
    seo_keywords = scrapy.Field()
    seo_description = scrapy.Field()
    origin = scrapy.Field()
    list_url = scrapy.Field()
    text = scrapy.Field()
    effective = scrapy.Field()

    version = scrapy.Field()
    left_img = scrapy.Field()
    down_url = scrapy.Field()
    likes = scrapy.Field()
    bd_down_url = scrapy.Field()
    size = scrapy.Field()
    downs = scrapy.Field()
    language = scrapy.Field()
    t_system = scrapy.Field()
    t_type = scrapy.Field()
    up_date = scrapy.Field()



class ArchivesItem(scrapy.Item):
    typeid = scrapy.Field()  # 当前栏目id
    title = scrapy.Field()  # 标题
    litpic = scrapy.Field()  # 缩略图
    origin = scrapy.Field()  # 来源
    author = scrapy.Field()  # 作者
    seo_title = scrapy.Field()  # SEO标题
    seo_keywords = scrapy.Field()  # SEO关键字
    seo_description = scrapy.Field()  # SEO描述


class ArctypeItem(scrapy.Item):
    id = scrapy.Field()  # 当前栏目id
    typename = scrapy.Field()  # 栏目名称
    seo_title = scrapy.Field()  # SEO标题
    seo_keywords = scrapy.Field()  # SEO关键字
    seo_description = scrapy.Field()  # SEO描述


class ContentItem(scrapy.Item):
    aid = scrapy.Field()  # 文档id
    content = scrapy.Field()  # 内容
