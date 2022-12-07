import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SteamspiderPipeline:
    def open_spider(self, spider):
        self.file = open('result.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item['publish_date'] and '0' <= item['publish_date'][-1] <= '9' and int(item['publish_date'][-4:]) > 2000:
            line = json.dumps(ItemAdapter(item).asdict()) + '\n'
            self.file.write(line)
        return item
