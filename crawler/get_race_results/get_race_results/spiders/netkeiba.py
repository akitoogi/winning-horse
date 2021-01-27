import scrapy
import json
from ..items import GetRaceResultsItem


class NetkeibaSpider(scrapy.Spider):
    name = 'netkeiba'
    allowed_domains = ['race.netkeiba.com']

    def start_requests(self):
        with open('start_url_list.txt') as f:
            for url in f:
                yield scrapy.Request(url.rstrip(), self.parse)

    def parse(self, response):
        #raceの情報を取得する。
        race_info_list = []
        race_info_dict = {}
        race_info_dict['name'] = response.xpath('//*[@class="RaceList_Item02"]/div/text()').get().strip()
        race_info_dict['time'] = response.xpath('//*[@class="RaceData01"]/text()[1]').get().strip()[:-2]
        race_info_dict['course'] = response.xpath('//*[@class="RaceData01"]/span[1]/text()').get().strip()
        race_info_dict['direction'] = response.xpath('//*[@class="RaceData01"]/text()[2]').get().strip()[1:2]
        race_info_dict['whether'] = response.xpath('//*[@class="RaceData01"]/text()[2]').get().strip()[-1:]
        race_info_dict['ground'] = response.xpath('//*[@class="RaceData01"]/span[3]/text()').get().strip()[-1:]
        race_info_dict['place'] = response.xpath('//*[@class="RaceData02"]/span[2]/text()').get().strip()
        race_info_dict['status'] = response.xpath('//*[@class="RaceData02"]/span[5]/text()').get().strip()
        race_info_dict['sex'] = response.xpath('//*[@class="RaceData02"]/span[6]/text()').get().strip()
        race_info_dict['age'] = response.xpath('//*[@class="RaceData02"]/span[7]/text()').get().strip()
        race_info_dict['number'] = response.xpath('//*[@class="RaceData02"]/span[8]/text()').get().strip()[:-1]
        race_info_list.append(race_info_dict)
        
        #raceの結果を取得する。
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