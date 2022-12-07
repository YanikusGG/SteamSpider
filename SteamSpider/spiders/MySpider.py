from http.client import responses
import scrapy
from SteamSpider.items import SteamspiderItem


class MyspiderSpider(scrapy.Spider):
    name = 'MySpider'
    allowed_domains = ['store.steampowered.com']
    start_urls = [
        'https://store.steampowered.com/search/?term=%D0%B3%D0%BE%D0%BD%D0%BA%D0%B8&category1=998&page=1', # гонки 1
        'https://store.steampowered.com/search/?term=%D0%B3%D0%BE%D0%BD%D0%BA%D0%B8&category1=998&page=2', # гонки 2
        'https://store.steampowered.com/search/?term=play&category1=998&page=1', # play 1
        'https://store.steampowered.com/search/?term=play&category1=998&page=2', # play 2
        'https://store.steampowered.com/search/?term=%D0%B3%D0%B5%D1%80%D0%BE%D0%B9&category1=998&page=1', # герой 1
        'https://store.steampowered.com/search/?term=%D0%B3%D0%B5%D1%80%D0%BE%D0%B9&category1=998&page=2', # герой 2
    ]

    def parse_game(self, response):
        item = SteamspiderItem()
        if response.xpath('//div[@class="age_gate"]/@class').extract_first():
            item['name'] = '18+ game'
            item['categorie'] = '18+'
            item['reviews_count'] = ''
            item['rating'] = ''
            item['publish_date'] = ''
            item['developer'] = 'bad boy'
            item['tags'] = '18+'
            item['price'] = ''
            item['platforms'] = ''
        else:
            item['name'] = response.xpath('//div[@id="appHubAppName"]/text()').extract_first().strip()
            item['categorie'] = ' > '.join(response.xpath('//div[@class="blockbg"]/a/text()').extract()[1:-1])
            item['reviews_count'] = (response.xpath('//div[@class="summary column"]/span[@class="responsive_hidden"]/text()').extract_first() or '').strip()
            item['rating'] = (response.xpath('//div[@class="summary column"]/span[contains(@class, "game_review_summary")]/text()').extract_first() or '').strip()
            item['publish_date'] = (response.xpath('//div[@class="release_date"]/div[@class="date"]/text()').extract_first() or '').strip()
            item['developer'] = response.xpath('//div[@id="developers_list"]/a/text()').extract()
            item['tags'] = ', '.join(t.strip() for t in response.xpath('//a[@class="app_tag"]/text()').extract())
            item['price'] = (response.xpath('//div[@class="game_purchase_price price"]/text()').extract_first() or '').strip()
            item['platforms'] = ', '.join(set(p[13:].strip() for p in response.xpath('//span[contains(@class,"platform_img")]/@class').extract()))
        yield item

    def parse(self, response):
        urls = response.xpath('//a[@class="search_result_row ds_collapse_flag "]/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_game)
