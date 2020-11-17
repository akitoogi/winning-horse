# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetRaceResultsItem(scrapy.Item):
    race_info = scrapy.Field()
    race_results = scrapy.Field()
