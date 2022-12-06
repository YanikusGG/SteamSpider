# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamspiderItem(scrapy.Item):
    name = scrapy.Field()
    categorie = scrapy.Field()
    reviews_count = scrapy.Field()
    rating = scrapy.Field()
    publish_date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()
