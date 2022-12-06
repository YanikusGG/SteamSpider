import scrapy
from SteamSpider.items import SteamspiderItem


class SpiderSpider(scrapy.Spider):
    name = 'Spider'
    allowed_domains = ['store.steampowered.com']
    start_urls = [
        'https://store.steampowered.com/search/?term=%D0%B3%D0%BE%D0%BD%D0%BA%D0%B8&page=1', # гонки 1
        'https://store.steampowered.com/search/?term=%D0%B3%D0%BE%D0%BD%D0%BA%D0%B8&page=2', # гонки 2
        'https://store.steampowered.com/search/?term=play&page=1', # play 1
        'https://store.steampowered.com/search/?term=play&page=2', # play 2
        'https://store.steampowered.com/search/?term=%D0%B3%D0%B5%D1%80%D0%BE%D0%B9&page=1', # герой 1
        'https://store.steampowered.com/search/?term=%D0%B3%D0%B5%D1%80%D0%BE%D0%B9&page=2', # герой 2
    ]

    def parse_game(self, response):
        item = SteamspiderItem()
        item['name'] = response.xpath('//div[@id="appHubAppName"]/text()').extract_first().strip()
        item['categorie'] = ' > '.join(response.xpath('//div[@class="blockbg"]/a/text()').extract())
        item['reviews_count'] = response.xpath('//div[@class="summary column"]/span[@class="responsive_hidden"]/text()').extract_first().strip()
        item['rating'] = response.xpath('//div[@class="summary column"]/span[contains(@class, "game_review_summary")]/text()').extract_first().strip()
        item['publish_date'] = response.xpath('//div[@class="release_date"]/div[@class="date"]/text()').extract_first().strip()
        item['developer'] = response.xpath('//div[@class="developers_list"]/a/text()').extract_first().strip()
        item['tags'] = ', '.join(response.xpath('//a[@class="app_tag"]/text()').extract())
        item['price'] = response.xpath('//div[@class="game_purchase_price price"]/text()').extract_first().strip()
        item['platforms'] = ', '.join(p[13:] for p in response.xpath('//span[contains(@class,"platform_img")]/@class').extract())
        yield item

    def parse(self, response):
        urls = response.xpath('//a[@class="search_result_row ds_collapse_flag  app_impression_tracked"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_game)
