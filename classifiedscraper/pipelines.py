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
import urllib.parse
from datetime import datetime, timedelta
import dateutil.parser


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
            logging.debug("Items to notify: " + str(len(items)))
            self._send_notification(items)


    def _send_notification(self, items):

        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))
        
        logging.info("Discord URL: " + self.discord_url)
        
        #Discord message gets to large, break it up
        for group in chunker(items, 5):
              
            for item in group:
                webhook = DiscordWebhook(url=self.discord_url, rate_limit_retry=True)
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
                embed.set_timestamp()

                # add fields to embed
                if item['location'] != None:
                  #https://www.google.com/maps/search/?api=1&query=centurylink+field
                  embed.add_embed_field(
                  name='Location', value="[" + str(item['location']) + "](https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(str(item['location'])) + ")" )
                if item['price'] != None:
                  embed.add_embed_field(name='Price', value=str(item['price']))
                if item['distance'] != None:
                  embed.add_embed_field(name='Distance', value=str(item['distance']))
                if item['source'] != None:
                  embed.add_embed_field(
                      #name='Source', value="[" + str(item['source']) + "](" + str(item['source_link']) + ")")
                      name='Source', value=str(item['source']))
                embed.add_embed_field(
                    name='Web Search', value="[Google](https://www.google.com/search?q=" + str(urllib.parse.quote(item['title'])) + ")")

                # add embed object to webhook
                webhook.add_embed(embed)
                
                #logging.debug("Discord webhook: " + str(webhook.json))
                
                try:
                    response = webhook.execute()
                except Timeout as err:
                    logging.error("Connection to Discord timed out: {err}")
                
                #10,000 per 10 minutes per discord api docs
                #sleep(0.75)
            

class KeywordFilterPipeline(object):

    def __init__(self, setting):
        self.keywords_file = setting
``
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
            found_item = self.db.get(collection['title'] == item['title'])
            logging.debug('Found Item in DB: ' +  found_item['title'])
            try:
                delta_time_last_seen = datetime.now() - dateutil.parser.parse(found_item['scraped_date'])
                logging.info(
                    'item last seen %s days ago', str(delta_time_last_seen.days))
                if delta_time_last_seen.days < 14:
                    logging.info("item seen recently: " + item['title'])
                    #drop the item as we've seen it recently
                    raise DropItem('recently seen item already in database: ' + item['title'])
                else:
                    logging.info('item not seen recently, updating item scraped date: '+ item['title'])
                    self.db.update(
                        {'scraped_date': str(datetime.now())}, collection['title'] == item['title'])

            except KeyError:
                logging.info('scraped_date key does not exist, adding now as the scraped date: '+ item['title'])
                self.db.update(
                    {'scraped_date': str(datetime.now())}, collection['title'] == item['title'])
            except TypeError:
                logging.info(
                    'scraped_date is not a string or date, adding now as the scraped date:' + item['title'])
                self.db.update(
                    {'scraped_date': str(datetime.now())}, collection['title'] == item['title'])

            
        #self.db.upsert(dict(item), collection.title == item['title'])
        else:
            logging.info('Added to DB: '+ item['title'])
            self.db.insert(dict(item))

        return item
