import scrapy
import re
import locale


class PropertiesSpider(scrapy.Spider):
    """Run 'scrapy crawl properties' in virtualenv"""
    name = 'properties'
    start_urls = ['https://www.finn.no/realestate/homes/search.html']

    def parse(self, response):
        for unit in response.css('div.ads__unit__content__keys'):
            keys = unit.css('*::text').getall()
            yield {
                'size': locale.atoi((re.sub('[^0-9,]', "", keys[0]))),
                'price': locale.atoi((re.sub('[^0-9,]', "", keys[1])))
            }
