
from scrapy import Spider
from ipagency.items import IpagencyItem
from pydispatch import dispatcher
from scrapy import signals


class XiciSpider(Spider):
    name = 'xici'
    allowed_domains = ["www.xicidaili.com"]
    start_urls = [
        'http://www.xicidaili.com/nn',
        'http://www.xicidaili.com/nt/',
        'http://www.xicidaili.com/wn/',
        'http://www.xicidaili.com/wt/'
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

#    def make_requests_from_url(self, url):
#        return Request(url=url, meta={"download_timeout": 30}, callback=self.parse)

    def parse(self, response, **kwargs):
        if response.url not in self.duplicates['url']:
            self.duplicates['url'].add(response.url)
            sites = response.xpath('//*[@id="ip_list"]/tr[position()>1]')
            for site in sites:
                item = IpagencyItem()
                protocol = site.xpath('td[6]/text()').extract_first()
                ip = site.xpath('td[2]/text()').extract_first()
                port = site.xpath('td[3]/text()').extract_first()
                item = {
                    "proxy": f"{protocol}://{ip}:{port}",
                    "country": site.xpath('td[1]/img/@alt').extract_first(default='Cn'),
                    "address": site.xpath('td[4]/a/text()').extract_first(default="not found"),
                    "anonymity": site.xpath('td[5]/text()').extract_first(),
                    "speed": site.xpath('td[7]/div/@title').extract_first(default="not found"),
                    "connect_time": site.xpath('td[8]/div/@title').extract_first(default="not found"),
                    "lifetime": site.xpath('td[9]/text()').extract_first(),
                    "proof": site.xpath('td[10]/text()').extract_first()
                }
                yield item

        link = response.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href')
        yield response.follow(url=link, callback=self.parse)
