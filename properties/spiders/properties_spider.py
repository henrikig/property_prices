import scrapy
import re
import locale


class PropertiesSpider(scrapy.Spider):
    """Run 'scrapy crawl properties' in virtualenv"""
    name = 'properties'
    allowed_domains = ['finn.no']
    start_urls = ['https://www.finn.no/realestate/homes/search.html']

    def parse(self, response):
        for unit in response.css('div.ads__unit__content__keys'):
            keys = unit.css('*::text').getall()
            if len(keys) > 1:
                yield {
                    'size': keys[0],
                    'price': keys[1]
                }

        for a in response.css('a.button--icon-right'):
            print('RESPONSE: ', a)
            yield response.follow(a, callback=self.parse)
