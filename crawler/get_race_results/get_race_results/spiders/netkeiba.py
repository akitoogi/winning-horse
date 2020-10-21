import scrapy


class NetkeibaSpider(scrapy.Spider):
    name = 'netkeiba'
    allowed_domains = ['https://race.netkeiba.com']
    start_urls = ['https://race.netkeiba.com/race/result.html?race_id=202008040411']

    def parse(self, response):
        for race_result in response.xpath('//*[@id="All_Result_Table"]/tbody/tr'):
            print('--------------------------------------')
            result = race_result.xpath('td/div').getall()
            print(result)