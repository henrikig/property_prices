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
        print("From pipeline:", item)
        item['size'] = re.sub(r'[^\x00-\x7F]+', '', item['size'])  # Remove non-ascii chars
        item['prize'] = locale.atoi((re.sub('[^0-9,]', "", item['price'])))  # Parse price
        return item
