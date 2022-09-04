
import scrapy
from ipagency.items import IpagencyItem


class GoubanjiaSpider(scrapy.Spider):
    name = 'goubanjia'
    allowed_domains = ["www.goubanjia.com"]
    start_urls = [
        'http://www.goubanjia.com/free/index.shtml'
    ]

    def __init__(self):
        super().__init__()
        self.duplicates = {}

    def parse(self, response, **kwargs):
        if response.url not in self.duplicates['url']:
            self.duplicates['url'].add(response.url)
            sites = response.xpath('//*[@id="list"]/table/tbody/tr')
            for site in sites:
                item = IpagencyItem()
                ip_port = "".join(site.xpath('td[1]//text()').extract())
                protocol = site.xpath('td[3]/a/text()').extract_first().lower()
                item = {
                    "proxy": f"{protocol}://{ip_port}",
                    "anonymity": site.xpath('td[2]/a/text()').extract_first(),
                    "address": {"address": site.xpath('td[4]/a/text()').extract()},
                    "operator": site.xpath('td[5]/text()').extract_first(),
                    "speed_time": site.xpath('td[6]/text()').extract_first(),
                    "proof_time": site.xpath('td[7]/text()').extract_first(),
                    "life_time": site.xpath('td[8]/text()').extract_first()
                }
                yield item

        links = response.xpath('//div[@class="wp-pagenavi"]/a/@href')
        for link in links:
            yield response.follow(url=link, callback=self.parse)
