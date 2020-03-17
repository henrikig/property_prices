# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import locale


class PropertiesPipeline(object):
    """{"size": "111 m\u00b2", "price": "2\u00a0900\u00a0000 kr"}"""
    def process_item(self, item, spider):
        item['size'] = (re.sub('[^0-9,-]', "", item['size'])).split("-")  # Remove non-ascii chars, split on hyphen
        item['price'] = (re.sub('[^0-9,-]', "", item['price'])).split("-")  # Parse price, split on hyphen

        item['size'][0] = int(item['size'][0])
        item['price'][0] = int(item['price'][0])

        if len(item['size']) > 1:
            item['size'][1] = int(item['size'][1])
        if len(item['price']) > 1:
            item['price'][1] = int(item['price'][1])

        return item
