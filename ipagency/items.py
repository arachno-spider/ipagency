# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IpagencyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    proxy = scrapy.Field()
    country = scrapy.Field()  # 国家
    address = scrapy.Field()
    method = scrapy.Field()
    #
    anonymity = scrapy.Field()  # 匿名
    speed_time = scrapy.Field()  # 响应时间
    proof_time = scrapy.Field()  # 验证时间
    life_time = scrapy.Field()  # 存活时间
    # 爬虫抓取相关
    source = scrapy.Field()  # 来源
    discovery_time = scrapy.Field()
