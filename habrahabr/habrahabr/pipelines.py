# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import pymongo
import requests


class ElasticsearchPipeline(object):
    """ Pipeline that sends data to AWS ES
    """

    def __init__(self, es_url, es_index, es_type):
        self.es_url = es_url
        self.es_index = es_index
        self.es_type = es_type

    @classmethod
    def from_crawler(cls, crawler):
        """ Creating ES pipeline using crawler's settings

        :param crawler:
        :return:
        """
        return cls(es_url=crawler.settings.get("ELASTICSEARCH_URL"),
                   es_index=crawler.settings.get("ELASTICSEARCH_INDEX"),
                   es_type=crawler.settings.get("ELASTICSEARCH_TYPE"))

    def process_item(self, item, spider):
        """

        :param item: <scrapy.Item>
        :param spider: <scrapy.Spider>
        :return:
        """

        # TODO. Format them normally!
        item["author"] = dict(item["author"])
        item["comments"] = dict(item["comments"])

        item_json = json.dumps(dict(item))
        url = "{}{}/{}/".format(self.es_url, self.es_index, self.es_type)
        response = requests.post(url, data=item_json)
        if response.status_code >= 200 and response.status_code < 300:
            print "Successfully sent data to ES"
        else:
            print "ERROR. Response: {}".format(response.content)
        return item


class MongoPipeline(object):
    """ Pipeline that stores data in MongoDB
    """

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        """ From documentation:

        If present, this classmethod is called to create a pipeline instance from a Crawler.
        It must return a new instance of the pipeline. Crawler object provides access to all
        Scrapy core components like settings and signals; it is a way for pipeline to access
        them and hook its functionality into Scrapy.
        """

        return cls(mongo_uri=crawler.settings.get("MONGO_URI"),
                   mongo_db=crawler.settings.get("MONGO_DATABASE"),
                   mongo_collection=crawler.settings.get("MONGO_COLLECTION"))

    def open_spider(self, spider):
        """ From documentation:

        This method is called when the spider is opened.

        :param spider: <scrapy.Spider>
        :return:
        """

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """ From documentation:

        This method is called when the spider is closed.

        :param spider: <scrapy.Spider>
        :return:
        """

        self.client.close()

    def process_item(self, item, spider):
        """ From documentation:

        This method is called for every item pipeline component and must either return a dict
        with data, Item (or any descendant class) object or raise a DropItem exception. Dropped
        items are no longer processed by further pipeline components.

        :param item: <scrapy.Item>
        :param spider: <scrapy.Spider>
        :return:
        """

        self.db[self.mongo_collection].insert(dict(item))
        return item
