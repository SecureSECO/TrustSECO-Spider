import scrapy

class LibrariesIoSpider(scrapy.Spider):
    name = 'Libraries.io'
    allowed_domains = ['libraries.io']
    start_urls = ['http://libraries.io/']

    def parse(self, response):
        pass
