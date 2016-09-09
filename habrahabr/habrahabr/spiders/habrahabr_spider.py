# -*- coding: utf-8 -*-
import scrapy

from habrahabr.items import *


class HabrahabrSpider(scrapy.Spider):
    name = "HabrahabrSpider"
    allowed_domains = ["habrahabr.ru"]
    start_urls = (
        'http://www.habrahabr.ru/',
    )

    def parse(self, response):
        for href in response.css(".post__title_link::attr('href')"):
            url = href.extract()
            print "HABRAHABR HOME PAGE PARSER: Received URL for article: {}".format(url)
            yield scrapy.Request(url, callback=self.parse_habra_article)

    def parse_habra_article(self, response):
        item = HabrahabrItem()

        item["article_title"] = response.css(".post__title span::text").extract()
        item["article_category"] = response.css(".post__flow::text").extract()
        item["article_hubs"] = response.css(".hub::text").extract()
        item["article_content"] = response.css(".post__title span::text").extract()
        item["article_tags"] = response.css(".post__title span::text").extract()

        item["author_name"] = response.css(".post__title span::text").extract()
        item["author_rating"] = response.css(".post__title span::text").extract()
        item["author_karma"] = response.css(".post__title span::text").extract()
        item["author_specialization"] = response.css(".post__title span::text").extract()

        item["comment_date"] = response.css(".post__title span::text").extract()
        item["comment_author"] = response.css(".post__title span::text").extract()
        item["comment_content"] = response.css(".post__title span::text").extract()

        # TODO: Translate NL datestamp to datetime. Ex: сегодня => datetime.today()
        item["article_date"] = response.css(".post__time_published::text").extract()
