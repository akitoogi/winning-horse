import scrapy
import json
from ..items import GetRaceResultsItem


class NetkeibaSpider(scrapy.Spider):
    name = 'netkeiba'
    allowed_domains = ['race.netkeiba.com']

    def start_requests(self):
        yield scrapy.Request('https://race.netkeiba.com/race/result.html?race_id=202106010101', self.parse)

    def parse(self, response):
        #obtain race information
        race_info_list = []
        race_info_a = response.xpath('//div[@class="RaceData01"]').get()
        race_info_b = response.xpath('//div[@class="RaceData02"]').get()
        race_info_list.append(race_info_a)
        race_info_list.append(race_info_b)


        #obtain race result
        race_result_list = []
        for race_result in response.xpath('//*[@id="All_Result_Table"]/tbody/tr'):
            race_result_dict = {}
            race_result_dict['rank'] = race_result.xpath('string(td[1]/div)').get().strip()
            race_result_dict['number'] = race_result.xpath('string(td[3]/div)').get().strip()
            race_result_dict['name'] = race_result.xpath('string(td[4]/span)').get().strip()
            race_result_dict['sex'] = race_result.xpath('string(td[5]//span)').get().strip()[0]
            race_result_dict['age'] = race_result.xpath('string(td[5]//span)').get().strip()[1]
            race_result_dict['jockey_weight'] = race_result.xpath('string(td[6]//span)').get().strip()
            race_result_dict['jockey_name'] = race_result.xpath('string(td[7]/a)').get().strip()
            race_result_dict['race_time'] = race_result.xpath('string(td[8]/span)').get().strip()

            race_time_diff = race_result.xpath('string(td[9]/span)').get().strip()
            if not race_time_diff:
                race_time_diff = 0
            race_result_dict['race_time_diff'] = race_time_diff

            race_result_dict['popularity'] = race_result.xpath('string(td[10]/span)').get().strip()
            race_result_dict['odds'] = race_result.xpath('string(td[11]/span)').get().strip()
            race_result_dict['last_time'] = race_result.xpath('string(td[12])').get().strip()
            race_result_dict['position'] = race_result.xpath('string(td[13])').get().strip()
            race_result_dict['place'] = race_result.xpath('string(td[14]/span)').get().strip()
            race_result_dict['trainer'] = race_result.xpath('string(td[14]/a)').get().strip()
            race_result_dict['weight'] = race_result.xpath('string(td[15])').get().strip()[:3]
            race_result_dict['weight_diff'] = race_result.xpath('string(td[15]/small)').get().strip()
            
            race_result_list.append(race_result_dict)
        
        yield {
            "race_info": race_info_list,
            "race_results": race_result_list
            }

        next_game = response.xpath('//*[@class="RaceNumWrap"]/ul/li[@class="Active"]/following-sibling::li/a/@href').get()
        next_place = response.xpath('//div[@class="RaceKaisaiWrap"]/ul/li[@class="Active"]/following-sibling::li/a/@href').get()

        if next_game:
            next_game_url = "https://race.netkeiba.com/race/result.html" + next_game
            yield scrapy.Request(next_game_url)
        elif next_place:
            next_game_url = "https://race.netkeiba.com/race/result.html" + next_place[:-2] + '01'
            yield scrapy.Request(next_game_url)
            
