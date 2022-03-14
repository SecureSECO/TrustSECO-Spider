# This file is not necessary

import scrapy

class LibrariesItem(scrapy.Item):
    contributors = scrapy.Field()
    releases = scrapy.Field()
    frequency_releases = scrapy.Field()
    latest_release_time = scrapy.Field()
    first_release_time = scrapy.Field()
    number_dependencies = scrapy.Field()
    number_dependent_packages = scrapy.Field()
    source_rank = scrapy.Field()

class LibrariesIoSpider(scrapy.Spider):
    name = 'libraries'
    start_urls = ['http://libraries.io/']

    def parse(self, response):
        pass
    
    def visit_page(self, response):
        item = LibrariesItem()
        contributors = 
