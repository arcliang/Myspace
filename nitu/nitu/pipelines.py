# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request

class NituPipeline(object):
    def process_item(self, item, spider):
        filename = item["url"].split('/')[-1]
        file = "F:/python/python项目/nitu_img/" + filename
        urllib.request.urlretrieve(item["url"], filename=file)
        return item
