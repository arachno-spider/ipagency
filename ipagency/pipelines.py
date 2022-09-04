# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from datetime import datetime, timedelta
import re
from tools.verify import request_verify, ipv4network


class IpagencyPipeline:
    def process_item(self, item, spider):
        if item and request_verify(item['proxy']):
            return item


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open(f'{spider.name}.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item:
            self.file.write(f"{item['proxy']}\n")
        return item


class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.client = MongoClient(f'mongodb://{mongo_uri}')
        self.db = self.client[mongo_db]
        self.client.list_databases()
        self.db.list_collections()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not item:
            return item

        # item = ItemAdapter(item)
        item = dict(item)
        item['_id'] = item['proxy']
        item['source'] = spider.name
        item['discovery_time'] = datetime.utcnow()
        item['expire_time'] = item['discovery_time'] + \
            timedelta(seconds=self._get_time(item.get('lifetime', "2天")))

        # col.ensure_index("expire_time", expireAfterSeconds=0)
        self.db.ip_proxy.create_index([('expire_time', 1)], expireAfterSeconds=0)
        if self.db.ip_proxy.count_documents({'_id': item['proxy']}) > 0:
            self.db.ip_proxy.update_one({"_id": item['proxy']}, {"$set": item})
        else:
            self.db.ip_proxy.insert_one(item)
        return item

    def _get_time(self, timestr):
        time_map = {
            "天": 24*3600,
            "小时": 3600,
            "分钟": 60
        }
        for timend in time_map.keys():
            if timend in timestr:
                timeint = int(re.match("\d+", timestr).group(0))
                expire_time = timeint * time_map[timend]
                return expire_time
        else:
            return time_map['小时'] * 5

