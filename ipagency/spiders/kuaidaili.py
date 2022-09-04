import scrapy
from ipagency.items import IpagencyItem


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    start_urls = [
        'https://free.kuaidaili.com/free/inha/',
        'https://free.kuaidaili.com/free/intr/'
    ]

    def __init__(self):
        super().__init__()
        self._index_links = set([])

    def parse(self, response, **kwargs):
        item = IpagencyItem()

        sites = response.xpath('//*[@id="list"]/table/tbody/tr')
        for site in sites:
            ip = site.xpath('td[@data-title="IP"]/text()').get().strip()
            port = site.xpath('td[@data-title="PORT"]/text()').get().strip()
            protocol = site.xpath('td[@data-title="类型"]/text()').get().strip().lower()
            item['proxy'] = f"{protocol}://{ip}:{port}"
            item['anonymity'] = site.xpath('td[@data-title="匿名度"]/text()').get().strip()
            item['address'] = {
                "address": site.xpath('td[@data-title="位置"]/text()').get().strip()
            }
            item['speed_time'] = site.xpath('td[@data-title="响应速度"]/text()').get().strip()
            item['proof_time'] = site.xpath('td[@data-title="最后验证时间"]/text()').get().strip()
            yield item

        link = response.xpath('//*[@id="listnav"]/ul/li/a[@class="active"]/../following-sibling::li[1]/a/@href').get()
        yield response.follow(link, callback=self.parse)

