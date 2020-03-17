import scrapy
import re
from ..constants import LOCATIONS


class PropertiesSpider(scrapy.Spider):
    """Run 'scrapy crawl properties' in virtualenv"""
    name = 'properties'
    allowed_domains = ['finn.no']
    start_urls = ['https://www.finn.no/realestate/homes/search.html?filters=' + parameter for parameter in LOCATIONS]

    def parse(self, response):
        parameter = response.request.url.split("filters=")[1][:17]
        location = LOCATIONS[parameter]

        for unit in response.css('div.ads__unit__content__keys'):
            keys = unit.css('*::text').getall()
            if len(keys) > 1:
                item = dict()
                # Remove non-ascii chars, split on hyphen
                item['size'] = (re.sub('[^0-9,-]', "", keys[0])).split("-")
                # Parse price, split on hyphen
                item['price'] = (re.sub('[^0-9,-]', "", keys[1])).split("-")

                item['size'][0] = int(item['size'][0])
                item['price'][0] = int(item['price'][0])

                if len(item['size']) > 1:
                    item['size'][1] = int(item['size'][1])
                if len(item['price']) > 1:
                    item['price'][1] = int(item['price'][1])

                item['location'] = location

                yield item

        for a in response.css('a.button--icon-right'):
            print('RESPONSE: ', a)
            yield response.follow(a, callback=self.parse)
