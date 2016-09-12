# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    """ Collecting content, tags, hubs, views and favourite counts info from habrahabr articles
    """

    # Id to identify article. It is extracted from article's URL
    # (ex. https://habrahabr.ru/company/<name>/blog/<id>/ = > _id = "company/<name>/blog/<id>"
    id = scrapy.Field()

    article_date        = scrapy.Field()
    article_category    = scrapy.Field()
    article_title       = scrapy.Field()
    article_hubs        = scrapy.Field()
    article_content     = scrapy.Field()
    article_tags        = scrapy.Field()
    article_url         = scrapy.Field()
    article_views       = scrapy.Field()
    article_favs        = scrapy.Field()

    author      = scrapy.Field()
    comments    = scrapy.Field()
