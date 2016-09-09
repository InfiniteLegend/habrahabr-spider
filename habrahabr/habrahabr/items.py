# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HabrahabrItem(scrapy.Item):
    """ Collecting content, tags, hubs, comments, author info from habrahabr articles

    """

    article_date        = scrapy.Field()
    article_category    = scrapy.Field()
    article_title       = scrapy.Field()
    article_hubs        = scrapy.Field()
    article_content     = scrapy.Field()
    article_tags        = scrapy.Field()

    author_name             = scrapy.Field()
    author_rating           = scrapy.Field()
    author_karma            = scrapy.Field()
    author_specialization   = scrapy.Field()

    comment_date    = scrapy.Field()
    comment_author  = scrapy.Field()
    comment_content = scrapy.Field()
