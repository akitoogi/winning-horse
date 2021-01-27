import scrapy
import json
from ..items import GetRaceResultsItem


class NetkeibaSpider(scrapy.Spider):
    def __init__(self):
        self.race_id_list = []

    name = 'get_start_url'
    allowed_domains = ['race.netkeiba.com', 'race.sp.netkeiba.com']

    def start_requests(self):
        yield scrapy.Request('https://race.sp.netkeiba.com/?pid=race_list&kaisai_date=20200105#racelist_top_a', self.parse)

    def parse(self, response):
        game_url = response.xpath('//div[@class="Contents_Box"]/div[position()=last()]/ul/li/div/a/@href').get()
        desired_start_url = 'https://race.netkeiba.com/race/result.html?race_id=' + game_url[-12:]
        self.race_id_list.append(desired_start_url + '\n')

        next_day = response.xpath('//div[@class="Tab_RaceDaySelect"]/ul/li/a[@class="Tab_Active"]/parent::li/following-sibling::li/a/@href').get()
        next_week = response.xpath('//div[@class="RaceDayNext"]/a/@href').get()
        if next_day:
            next_day_url = 'https://race.sp.netkeiba.com/' + next_day
            yield scrapy.Request(next_day_url)
        elif next_week:
            next_week_url = 'https://race.sp.netkeiba.com/' + next_week
            yield scrapy.Request(next_week_url)
        else:
            with open('start_url_list.txt', 'w') as f:
                f.writelines(self.race_id_list)
