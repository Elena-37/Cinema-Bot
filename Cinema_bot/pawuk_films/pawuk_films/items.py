# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PawukFilmsItemLord(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    country = scrapy.Field()
    genres = scrapy.Field()
    rating_kp = scrapy.Field()
    rating_imdb = scrapy.Field()
    film_or_series = scrapy.Field()
    poster = scrapy.Field()

class PawukFilmsItemIvi(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    country = scrapy.Field()
    genres = scrapy.Field()
    rating_ivi = scrapy.Field()
    film_or_series = scrapy.Field()
    poster = scrapy.Field()

class PawukFilmsItemKino(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    country = scrapy.Field()
    genres = scrapy.Field()
    rating_kp = scrapy.Field()
    rating_imdb = scrapy.Field()
    film_or_series = scrapy.Field()
    poster = scrapy.Field()