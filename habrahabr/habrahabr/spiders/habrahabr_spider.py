# -*- coding: utf-8 -*-
import scrapy

from habrahabr.items import ArticleItem
from habrahabr.utils import extract_id_from_url, translate_number, translate_date


class HabrahabrSpider(scrapy.Spider):
    name = "HabrahabrSpider"
    allowed_domains = ["habrahabr.ru"]
    start_urls = ["http://www.habrahabr.ru/page{}/".format(i) for i in xrange(1, 101)]
    parsed_articles_count = 0

    def parse(self, response):
        parsed_articles = []
        for href in response.css(".post__title_link::attr('href')"):
            url = href.extract()
            if url not in parsed_articles:
                print "HABRAHABR HOME PAGE PARSER: Received URL for article: {}".format(url)
                self.parsed_articles_count += 1
                parsed_articles.append(url)
                yield scrapy.Request(url, callback=self.parse_habra_article)
        print "HABRAHABR PARSER: {} pages successfully parsed!".format(self.parsed_articles_count)

    def parse_habra_article(self, response):
        article = ArticleItem()
        url = response.url

        try:
            # Extracting _id
            article["id"] = extract_id_from_url(url)

            # Parsing article details
            print "HABRAHABR ARTICLE PARSER: Parsing article"
            article["article_title"]       = unicode(response.css(".post__title span:not([class])::text").extract()[0])
            article["article_category"]    = unicode(response.css(".post__flow::text").extract()[0])
            article["article_hubs"]        = [unicode(hub) for hub in response.css(".hub::text").extract()]
            article["article_content"]     = " ".join([unicode(html.strip()) for html in response.css(".html_format::text").extract()
                                                       if html.strip()])
            article["article_tags"]        = response.css(".post__tags li a::text").extract()
            article["article_favs"]        = translate_number(response.css(".favorite-wjt__counter::text").extract()[0])
            article["article_url"]         = url

            # Parsing article's author info
            print "HABRAHABR ARTICLE PARSER: Parsing author info"
            # TODO: Correctly parse float values, ignoring whitespaces (ex. "1 233")
            try:
                karma = response.css(".voting-wjt__counter-score::text").extract()
                specialization = response.css(".author-info__specialization::text").extract()
                translate_number(karma[0])
            except Exception:
                print "HABRAHABR ARTICLE PARSER: Unable to parse KARMA or SPECIALIZATION field"

            # Extracting author info
            author = dict()
            author["karma"]          = translate_number(karma[0]) if karma else "No karma"
            author["specialization"] = [unicode(" ".join(html.split())) for html in response.css(".author-info__specialization::text").extract()] if \
                specialization else "Company"
            author["name"]           = unicode((response.css(".author-info__name::text").extract() or
                                                response.css(".author-info__nickname::text").extract() or
                                                response.css(".author-info__username::text").extract())[0])
            author["rating"]         = translate_number(response.css(".user-rating__value::text").extract()[0])

            # Assigning gotten data to author field
            article["author"] = author

            # Assigning empty list of comments to article
            article["comments"] = list()

            for comment_obj in response.css(".comment_item"):
                print "HABRAHABR ARTICLE PARSER: Parsing comment"
                comment = dict()

                # TODO: Translate NL datestamp to datetime. Ex: 9 сентября 2016 в 10:08 => datetime.now()
                comment["date"]     = translate_date(comment_obj.css("time::text").extract()[0])
                comment["author"]   = unicode(comment_obj.css(".comment-item__username::text").extract()[0])
                comment["content"]  = unicode(comment_obj.css(".message::text").extract()[0].strip())

                # Appending comment to article
                article["comments"].append(comment)

            # TODO: Translate NL datestamp to datetime. Ex: сегодня => datetime.today()
            article["article_date"] = translate_date(response.css(".post__time_published::text").extract()[0])

            article["article_views"]       = translate_number(response.css(".views-count_post::text").extract()[0])
        except IndexError, exc:
            print "HABRAHABR ARTICLE PARSER: Unable to parse element in article '{}'. Error: {}".format(url, exc)
        except Exception, exc:
            print "HABRAHABR ARTICLE PARSER: Unknown error occurred. Error: {}".format(exc)
        else:
            yield article
