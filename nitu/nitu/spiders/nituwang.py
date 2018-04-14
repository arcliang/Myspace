# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from nitu.items import NituItem

class NituwangSpider(scrapy.Spider):
    name = 'nituwang'
    allowed_domains = ['nipic.com']
    start_urls = ['http://nipic.com/']
    #第一层链接
    def parse(self, response):
        Frist_url = response.xpath('//div[@class="newIndex-nav-condition fl"]/a/@href').extract()
        True_url = Frist_url[2:5]
        for i in range(len(True_url)):
            TrueTrue_url = "http://www.nipic.com/" + True_url[i]
            yield Request(url=TrueTrue_url,callback=self.next1)
    #第二层链接
    def next1(self,response):
        Second_url = response.xpath('//dd[@class="menu-item-list clearfix"]//a/@href').extract()

        for m in range(len(Second_url)):
            Second_true_url = "http://www.nipic.com/" + Second_url[m]
            yield Request(url=Second_true_url,meta={'key':Second_true_url},callback=self.next2)
    def next2(self,response):
        #查找总页数
        page_num = response.xpath('//div[@class="common-page-box mt10 align-center"]/a/@href').extract()
        page_true_num = page_num[-1].split('=')[-1]


        for n in range(1,int(page_true_num)+1):
            page_url = str(response.meta['key']) + "?page=" + str(n)
            yield Request(url=page_url,callback=self.next3)
    #第三层链接
    def next3(self,response):
        img_url = response.xpath('//li[@class="works-box mb17 fl"]/div[@class="search-works-info"]/a/@href').extract()
        for k in range(len(img_url)):
            yield Request(url=img_url[k],callback=self.next4)
    #获取大图的链接
    def next4(self,response):
        img_big_url = response.xpath('//div[@class="show-img-section overflow-hidden align-center"]/img/@src').extract()[0]
        item = NituItem()
        item['url'] = img_big_url
        yield item



