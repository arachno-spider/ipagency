# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from pymongo import MongoClient
from fake_useragent import UserAgent
import time


class IpagencySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class IpagencyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class IPMongoProxyMiddleware(object):
    def __init__(self, mongo_uri, mongo_db):
        self.client = MongoClient(f'mongodb://{mongo_uri}')
        self.db = self.client[mongo_db]
        print(self.client.list_databases())
        print(self.db.list_collections())

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def process_request(self, request, spider):
        """对request对象加上proxy"""
        ip_proxy = self.get_random_proxy()
        # time.sleep(3)
        if ip_proxy is not None:
            request.meta['proxy'] = ip_proxy
            print("this is request ip:" + request.meta['proxy'])
        else:
            print("The request proxy is None")

    def process_response(self, request, response, spider):
        """对返回的response处理"""
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            # 删除当前代理ip
            # self.db.ip_proxy.remove({"proxy": request.meta['proxy']})
            # 获取新ip代理
            ip_proxy = self.get_random_proxy()
            # 对当前request加上代理
            if ip_proxy is not None:
                request.meta['proxy'] = ip_proxy
                print("this is response ip:" + request.meta['proxy'])
            else:
                print("The response proxy is None")
            return request
        # time.sleep(1)
        return response

#    def process_exception(self, request, exception, spider):
#        # self.logger.info("Get Exception")
#        request.meta['request'] = "http://127.0.0.1:9743"
#        print("this is exception ip:" + request.meta['request'])
#        return request

    def get_random_proxy(self):
        """随机读取ip proxy"""
        query = {
            "ip_port": {"$exists": True},
            "anonymity": "高匿"
        }
        item = self.db.ip_proxy.find(query, {"_id": 0}).limit(1)
        return item['proxy']


class RandomUserAgentMiddleWare(object):
    """
    随机更换User-Agent
    """
    def __init__(self, crawler):
        super().__init__()
        self.ua = UserAgent(verify_ssl=False)
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua_type():
            # 取对象 ua 的 ua_type 的这个属性, 相当于 self.ua.self.ua_type
            return getattr(self.ua, self.ua_type)

        # request.headers.setdefault('User-Agent', get_ua_type())
        request.headers['User-Agent'] = get_ua_type()
        # request.headers['Connection'] = "close"
