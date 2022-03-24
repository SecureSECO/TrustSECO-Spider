import scrapy
from scrapy import Field, Item

class CVESpider(scrapy.Spider):
    name = 'Ubuntu'
    start_urls = [str('https://ubuntu.com/security/notices?order=newest&release=&details=') + str(input('Enter the keyword to search on for Ubuntu security notices:'))]

    def parse(self, response):
        links = response.css('article.notice h3 a::attr(href)').getall()
        for link in links:
            yield scrapy.Request('https://ubuntu.com' + str(link), callback=self.scrape_vulnerabilities)
        
        next_page = response.css('a.p-pagination__link--next::attr(href)').get()
        if next_page:
            next_page_url = 'https://ubuntu.com/security/notices' + next_page
            yield scrapy.Request(url=next_page_url)

    def scrape_vulnerabilities(self, response):
        item = UbuntuItem()
        item['url'] = response.url
        item['title'] = response.css('.col-12 h1::text').get()
        item['date'] = response.css('.col-12 p::text').getall()[0]
        item['short_description'] = response.css('.col-12 p::text').getall()[1].strip()
        item['details'] = response.css('.col-8').get()
        try:
            packages = response.css('.col-12').getall()[2]
            item['packages'] = packages
        except Exception:
            item['packages'] = ''
        item['update_instruction'] = response.css('.col-8').get()
        yield item
    
class UbuntuItem(scrapy.Item):
        url = Field()
        title = Field()
        date = Field()
        short_description = Field()
        update_instruction = Field()
        packages = Field()
        details = Field()