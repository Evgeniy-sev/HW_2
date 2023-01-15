# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class NotebooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NotebookItem(Item):
    url = Field()
    visited_at = Field()
    name = Field()
    cpu_hhz = Field()
    ram_gb = Field()
    ssd_gb = Field()
    price_rub = Field()
    rank = Field()
    
