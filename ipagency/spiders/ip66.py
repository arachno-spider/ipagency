import scrapy
from scrapy.http import Request
from ipagency.items import IpagencyItem
from pydispatch import dispatcher
from scrapy import signals


class Ip66Spider(scrapy.Spider):
    name = 'ip66'
    allowed_domains = ["www.66ip.cn"]
    start_urls = [
        'http://www.66ip.cn'
    ]

    def __init__(self):
        super().__init__()
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self):
        self.duplicates['url'] = set()

    def spider_closed(self):
        del self.duplicates['url']

    def parse(self, response, **kwargs):
        sites = response.xpath('//ul[@class="textlarge22"]/li[position()>1]/a')
        for site in sites:
            link = site.xpath('@href')
            province = site.xpath('text()').extract_first()
            yield response.follow(link, meta={'province': province})

    def parse_content(self, response):
        if response.url not in self.duplicates['url']:
            self.duplicates['url'].add(response.url)
            item = IpagencyItem()
            sites = response.xpath('//*[@class="main"]/div/div[1]/table/tr[position()>1]')
            for site in sites:
                ip = site.xpath('td[1]/text()').get()
                port = site.xpath('td[2]/text()').extract_first()
                item['proxy'] = f"http://{ip}:{port}"
                item['address'] = {
                    "address": site.xpath('td[3]/text()').extract_first(),
                    "province": response.meta['province']
                }
                item['anonymity'] = site.xpath('td[4]/text()').extract_first()
                item['proof_time'] = site.xpath('td[10]/text()').extract_first()
                yield item
        link = response.xpath('//*[@id="PageList"]/a[-1]/@href').extract_first()
        yield Request(link, callback=self.parse_content)
