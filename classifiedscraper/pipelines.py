# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
import logging
from tinydb import TinyDB, Query
from random import randint
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed


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
        
        
        
        #Discord message gets to large, break it up
        for group in chunker(items, 5):
              
#             # jinja template
#             from jinja2 import Template
#             template = Template(
#             """
#             {% for item in items %}
# [{{item['title']}}]({{item['link']}}) - {{item['price']}} - {{item['location']}}
#             {% endfor %}
#             """
#             )

#             content = template.render(items=group)
#             logging.info("content: %s",content)
            
#             #send discord
#             webhook = DiscordWebhook( 
#                 url=self.discord_url, content=content)
#             response = webhook.execute()
            #don't crush the webhook

            for item in group:
                webhook = DiscordWebhook(url=self.discord_url)
                # create embed object for webhook
                embed = DiscordEmbed(title=item['title'], url=item['link'])

                # set author
                #embed.set_author(name='Classified Scraper')

                # set image
                if item['image_link'] != None:
                    embed.set_image(url=item['image_link'])

                    # set thumbnail
                    # embed.set_thumbnail(url=item['image_link'])

                # set timestamp (default is now)
                #embed.set_timestamp()

                # add fields to embed
                if item['location'] != None:
                  embed.add_embed_field(name='Location', value=item['location'])
                if item['price'] != None:
                  embed.add_embed_field(name='Price', value=item['price'])
                if item['distance'] != None:
                  embed.add_embed_field(name='Distance', value=item['distance'])

                # add embed object to webhook
                webhook.add_embed(embed)

                response = webhook.execute()
                sleep(randint(1, 10))
            




class KeywordFilterPipeline(object):
    #TODO: Externalize this list to a file

    def __init__(self, setting):
        self.keywords_file = setting

        logging.info("keywords file: %s", self.keywords_file)

        with open(self.keywords_file, "rt") as f:
          self.keywords = [line.strip() for line in f.readlines()]

        logging.info("keywords: %s", self.keywords)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            setting=crawler.settings.get('FILTER_KEYWORDS_FILE')
        )


    def process_item(self, item, spider):
        try:
            if any(key in item['title'].lower() for key in self.keywords):
                raise DropItem('filter keyword found')
        except Exception:
            pass
        return item


class PersistancePipeline(object):
    

    def __init__(self, tiny_db):
        self.tiny_db = tiny_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            tiny_db=crawler.settings.get('TINY_DB_FILE')
        )

    def open_spider(self, spider):
        self.db = TinyDB(self.tiny_db)

    def close_spider(self, spider):
        logging.info('TinyDB Size: %s', str(len(self.db)))

    def process_item(self, item, spider):
        collection = Query()
        #TODO Check for price drops
        if self.db.contains(collection['title'] == item['title']):
            raise DropItem('Item already in database')
        
        #self.db.upsert(dict(item), collection.title == item['title'])
        logging.info('Added to DB')
        self.db.insert(dict(item))

        return item
