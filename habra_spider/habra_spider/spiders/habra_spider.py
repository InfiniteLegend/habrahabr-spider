# -*- coding: utf-8 -*-
import scrapy


class HabraSpider(scrapy.Spider):
    name = "HabraSpider"
    allowed_domains = ["habrahabr.ru"]
    start_urls = (
        'http://www.habrahabr.ru/',
    )

    def parse(self, response):
        for href in response.css(".post__title_link::attr('href')"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_habra_article)

    def parse_habra_article(self, response):
        print response.css(".post__title span::text").extract()
