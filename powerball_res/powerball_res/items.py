from scrapy.item import Item, Field


class PowerballResItem(Item):
    game = Field()
    draw_date = Field()
    jackpot = Field()
    results = Field()
