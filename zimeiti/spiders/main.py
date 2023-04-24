import scrapy

class MainSpider(scrapy.Spider):
    # name = "main"
    allowed_domains = ["xxx.com"]
    start_urls = ["http://xxx.com/"]

    def parse(self, response):
        pass
