import scrapy
from ipagency.items import IpagencyItem


class YundailiSpider(scrapy.Spider):
    name = 'yundaili'
    allowed_domains = ['ip3366.net']
    start_urls = ['http://www.ip3366.net/']

    def parse(self, response, **kwargs):
        item = IpagencyItem()
        sites = response.xpath('//*[@id="list"]/table/tbody/tr')
        for site in sites:
            protocol = site.xpath('td[4]/text()').get().strip().lower()
            ip = site.xpath('td[1]/text()').get().strip()
            port = site.xpath('td[2]/text()').get().strip()
            item['proxy'] = f"{protocol}://{ip}:{port}"
            item['anonymity'] = site.xpath('td[3]/text()').get().strip()
            item['method'] = site.xpath('td[5]/text()').get().strip()
            item['address'] = site.xpath('td[6]/text()').get().strip()
            item['speed_time'] = site.xpath('td[7]/text()').get().strip()
            item['proof_time'] = site.xpath('td[8]/text()').get().strip()
            yield item
        link = response.xpath('//*[@id="listnav"]/ul/a[text()="下一页"]/@href').get()
        yield response.follow(link, self.parse)
