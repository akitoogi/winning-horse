import scrapy


class NetkeibaSpider(scrapy.Spider):
    name = 'netkeiba'
    allowed_domains = ['https://race.netkeiba.com']
    start_urls = ['https://race.netkeiba.com/top/']

    def parse(self, response):
        pass