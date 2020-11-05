# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
import logging


class ClassifiedscraperPipeline:
    def process_item(self, item, spider):
        return item


class SendDiscordPipeline(object):
    def __init__(self, discord_url):
        self.items_cache = []
        # self.cache_size = 0
        self.discord_url = discord_url
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        discord_url = settings['DISCORD_NOTIFICATION_URL']
        return cls(discord_url)

    def process_item(self, item, spider):
        self.items_cache.append(item)
        return item

    def close_spider(self, spider):
        # When the spider is finished, we need to flush the cache one last
        # time to make sure that all items are sent
        self._flush_cache()

    def _flush_cache(self):
        items = self.items_cache

        if len(items) > 0:
            self.items_cache = []  # reset cache to empty
            self._send_notification(items)


    def _send_notification(self, items):

        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        for group in chunker(items, 5):
            
            # jinja template
            from jinja2 import Template
            template = Template(
            """
            {% for item in items %}
[{{item['title']}}]({{item['link']}}) - {{item['price']}} - {{item['location']}}
            {% endfor %}
            """
            )

            content = template.render(items=group)
            logging.info("content: %s",content)
            
            #send discord
            from discord_webhook import DiscordWebhook
            webhook = DiscordWebhook( 
                url=self.discord_url, content=content)
            response = webhook.execute()


class KeywordFilterPipeline(object):

    keywords = ['wanted', 'tandem', 'electric', 'cruiser', 'recumbent', 'trathalon', 'road']

    def process_item(self, item, spider):
        if any(key in item['title'].lower() for key in self.keywords):
            raise DropItem('filter keyword found')
        return item
