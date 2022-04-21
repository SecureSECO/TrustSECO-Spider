import scrapy
from scrapy import Field, Item


class CVESpider(scrapy.Spider):
    name = 'CVE'
    start_urls = [str('https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=') +
                  str(input('Enter the keyword to search on for security vulnerabilities:'))]

    def parse(self, response):
        links = response.css('a::attr(href)').getall()
        for link in links:
            if link.startswith('/cgi-bin/'):
                yield scrapy.Request('https://cve.mitre.org/' + str(link), callback=self.scrape_vulnerabilities)

    def scrape_vulnerabilities(self, response):
        item = CVEItem()
        item['CVE_ID'] = response.css('h2::text').get()
        item['CVE_vulnerability_description'] = response.css('td').getall(
        )[10].replace('<td colspan="2">', '').replace('</td>', '').strip()
        date = response.css('b::text').getall()[1]
        date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
        item['record_date'] = date
        item['CVE_link'] = response.url
        yield item


class CVEItem(scrapy.Item):
    CVE_ID = Field()
    record_date = Field()
    CVE_vulnerability_description = Field()
    CVE_link = Field()
