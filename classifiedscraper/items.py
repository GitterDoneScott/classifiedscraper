# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from scrapy.loader.processors import MapCompose, TakeFirst
import scrapy
from datetime import datetime


def parse_location(text):
    # parse location "Charlotte, North Carolina, United States"
    logging.info("location: %s", text)
    text.strip()
    logging.info("location: %s", text)
    separator = ','
    text = text.split(sep, 1)[0]
    logging.info("location: %s", text)
    text = text + "fasfasdfasdfadsf"
    return text

class ClassifiedscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    location = scrapy.Field()
    distance = scrapy.Field()
    description = scrapy.Field()
    image_link = scrapy.Field()
    source = scrapy.Field()
    post_date = scrapy.Field()
    source_link = scrapy.Field()
    scraped_date = scrapy.Field()
    pass

    def set_all(self, value):
        for keys, _ in self.fields.items():
            self[keys] = value
        self['scraped_date'] = str(datetime.now())

# @dataclass
# class ClassifiedscraperItem:
#     title: str
#     price: str
#     link: str
#     location: str
#     description: str
#     image_link: str
