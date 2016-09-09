# -*- coding: utf-8 -*-
import scrapy

from habrahabr.items import ArticleItem, AuthorItem, CommentItem


class HabrahabrSpider(scrapy.Spider):
    name = "HabrahabrSpider"
    allowed_domains = ["habrahabr.ru"]
    start_urls = ["http://www.habrahabr.ru/page{}/".format(i) for i in xrange(1, 101)]

    def parse(self, response):
        parsed_articles_count = 0
        parsed_articles = []
        for href in response.css(".post__title_link::attr('href')"):
            url = href.extract()
            if url not in parsed_articles:
                print "HABRAHABR HOME PAGE PARSER: Received URL for article: {}".format(url)
                parsed_articles_count += 1
                parsed_articles.append(url)
                yield scrapy.Request(url, callback=self.parse_habra_article)
        print "HABRAHABR PARSER: {} pages successfully parsed!".format(parsed_articles_count)

    def parse_habra_article(self, response):
        article = ArticleItem()
        author = AuthorItem()

        try:
            # Parsing article details
            article["article_title"]       = unicode(response.css(".post__title span:not([class])::text").extract()[0])
            article["article_category"]    = unicode(response.css(".post__flow::text").extract()[0])
            article["article_hubs"]        = [unicode(hub) for hub in response.css(".hub::text").extract()]
            article["article_content"]     = " ".join([unicode(html.strip()) for html in response.css(".html_format::text").extract()
                                                       if html.strip()]); article["article_tags"]        = response.css(".post__tags li a::text").extract()
            article["article_favs"]        = response.css(".favorite-wjt__counter::text").extract()[0]
            article["article_url"]         = response.url

            # Parsing article's author info
            karma = response.css(".voting-wjt__counter-score::text").extract()
            specialization = response.css(".author-info__specialization::text").extract()
            author["author_karma"]          = float(karma[0].replace(",", ".")) if karma else "No karma"
            author["author_specialization"] = unicode(specialization[0]) if specialization else "Company"
            author["author_name"]           = unicode(response.css(".post-additionals .author-info__name::text").extract()[0])
            author["author_rating"]         = float(response.css(".user-rating__value::text").extract()[0].replace(",", "."))

            # Assigning author to article
            article["author"] = author

            # Assigning empty list of comments to article
            article["comments"] = list()

            for comment_obj in response.css(".comment_item"):
                comment = CommentItem()

                # TODO: Translate NL datestamp to datetime. Ex: 9 сентября 2016 в 10:08 => datetime.now()
                comment["comment_date"]     = unicode(comment_obj.css("time::text").extract()[0])
                comment["comment_author"]   = unicode(comment_obj.css(".comment-item__username::text").extract()[0])
                comment["comment_content"]  = unicode(comment_obj.css(".message html_format ::text").extract()[0])

                # Appending comment to article
                article["comments"].append(comment)

            # TODO: Translate NL datestamp to datetime. Ex: сегодня => datetime.today()
            article["article_date"] = unicode(response.css(".post__time_published::text").extract()[0])

            article["article_views"]       = response.css(".views-count_post::text").extract()[0]
        except IndexError, exc:
            print "HABRAHABR ARTICLE PARSER: Unable to parse element in article '{}'. Error: {}".format(response.url, exc)
        except Exception, exc:
            print "HABRAHABR ARTICLE PARSER: Unknown error occurred. Error: {}".format(exc)
        else:
            yield article
