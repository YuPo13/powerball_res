"""This module describes behaviour of 'regular' spider created for lottery results scraping"""
from powerball_res.items import PowerballResItem
from scrapy.spiders import Spider
from scraping_dates import url_for_scraping
from lxml import etree


class PowerballResults(Spider):
    """This class represents the scraping instance"""
    name = "alternative_powerball_spider"
    allowed_domains = ["lottery.com"]
    start_urls = [
        url_for_scraping
    ]

    custom_settings = {
        'FEED_URI': "powerball_3months_results.csv"
    }

    def parse(self, response):
        """This function provides the mechanism for relevant data extraction and saving to csv file"""
        abstract_for_scraping = response.xpath('//*[@class="lottery-vertical-view-items clearfix"]').getall() + \
                                response.xpath('//*[@class="lottery-vertical-view-items clearfix hidden"]').getall()

        for passage in abstract_for_scraping:
            html_tree = etree.HTML(passage)
            item = PowerballResItem()
            item["game"] = html_tree.xpath('//*[@class="title-column"]/text()')
            item['draw_date'] = html_tree.xpath('//*[@class="date-column"]/div/text()')
            item['jackpot'] = html_tree.xpath('//*[@class="jackpot-column"]/span/text()')
            item['results'] = html_tree.xpath('//*[@class="results-column"]/div[@class="lottery-item-winnumbers"]/'
                                           'div[@class="lottery-ball-wrap"]/div/span/text()')
            yield item
