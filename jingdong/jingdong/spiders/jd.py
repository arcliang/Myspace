# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from jingdong.items import JingdongItem
import re
import urllib

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']

    def parse(self, response):
        key = "笔记本"
        search_url = "https://search.jd.com/Search?keyword=" + key + "&enc=utf-8&wq=" + key
        for i in range(1,101):
            page_url = search_url + "&page=" + str(i*2-1)
            yield Request(url=page_url,callback=self.next)
    def next(self,response):
        id = response.xpath('//ul[@class="gl-warp clearfix"]/li/@data-sku').extract()
        #print(id)
        for j in range(len(id)):
            ture_url = "https://item.jd.com/" + str(id[j]) + ".html"
            yield Request(url=ture_url,callback=self.next2)
    def next2(self,response):
        item = JingdongItem()
        item['title'] = response.xpath('//head/title/text()').extract()[0].replace('【图片 价格 品牌 报价】-京东','').replace('【行情 报价 价格 评测】-京东','')
        item['link'] = response.url
        #价格抓包
        ture_id = re.findall(r'https://item.jd.com/(.*?).html',item['link'])[0]
        price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + str(ture_id)
        price_txt = urllib.request.urlopen(price_url).read().decode('utf-8', 'ignore')
        item['price'] = re.findall(r'"p":"(.*?)"',price_txt)[0]
        #评论抓包
        comment_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + str(ture_id)
        comment_txt = urllib.request.urlopen(comment_url).read().decode('utf-8', 'ignore')
        item['comment'] = re.findall(r'"CommentCount":(.*?),"',comment_txt)[0]
        return item

