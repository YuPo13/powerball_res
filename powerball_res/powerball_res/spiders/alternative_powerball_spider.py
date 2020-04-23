"""This module describes behaviour of 'alternative' spider created for lottery results scraping"""
from powerball_res.items import PowerballResItem
from scrapy.spiders import Spider
from scraping_dates import url_for_scraping


class PowerballResults(Spider):
    """This class represents the scraping instance"""
    name = "alternative_powerball_spider"
    allowed_domains = ["lottery.com"]
    start_urls = [
        url_for_scraping
    ]

    custom_settings = {
        'FEED_URI': "alt_powerball_3months_results.csv"
    }

    def parse(self, response):
        """This function provides the mechanism for relevant data extraction and saving to csv file"""
        games = response.xpath('//*[@class="title-column"]/text()').getall()
        draw_dates = response.xpath('//*[@class="date-column"]/div/text()').getall()
        jackpots = response.xpath('//*[@class="jackpot-column"]/span/text()').getall()
        raw_results = response.xpath('//*[@class="results-column"]/div[@class="lottery-item-winnumbers"]/'
                                         'div[@class="lottery-ball-wrap"]/div/span/text()').getall()
        results = [raw_results[x:x+6] for x in range(0, len(raw_results), 6)]

        final_dataset = zip(games, draw_dates, jackpots, results)

        for data_piece in final_dataset:
            item = PowerballResItem()
            item["game"] = data_piece[0]
            item['draw_date'] = data_piece[1]
            item['jackpot'] = data_piece[2]
            item['results'] = data_piece[3]
            yield item
