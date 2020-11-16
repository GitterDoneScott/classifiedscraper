# pyenv install 3.7.7
# pyenv local 3.7.7
# pipenv -python 3.7.7
# pipenv install requests-html
# pipenv shell
# scrapy startproject <project>
# scrapy crawl pinkbike
# scrapy shell "https://www.pinkbike.com/buysell/list/?lat=34.8646&lng=-82.0469&distance=150&q=title:%20Jeffsy%20OR%20trance%20OR%20frame&wheelsize=10"

import scrapy
from scrapy.utils.markup import remove_tags
from ..items import ClassifiedscraperItem
import logging


class PinkbikeSpider(scrapy.Spider):
    name = "pinkbike"

    def __init__(self, urls_file):
        self.urls_file = urls_file

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            urls_file=crawler.settings.get('PINKBIKE_URLS_FILE')
        )

    def start_requests(self):

        logging.info("url file: %s", self.urls_file)

        with open(self.urls_file, "rt") as f:
          start_urls = [url.strip() for url in f.readlines()]

         #dont_filter bypasses the duplicate url filter
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for item in response.css('div.bsitem > table  > tr'):
            #self.logger.info("Found:", item)
            adItem = ClassifiedscraperItem()
            adItem.set_all(None)
            adItem['source'] = self.name
            adItem['title'] = item.css(
                'td:nth-child(2) > div > a::text').get()
            adItem['link'] = item.css(
                'td:nth-child(2) >div > a::attr(href)').get()
            #csid2904951 > table > tbody > tr > td:nth-child(1) > ul > li > a > img
            adItem['image_link'] = item.css(
                'td:nth-child(1) > ul > li > a > img::attr(src)').get()
            location_raw = remove_tags(item.css(
                'td:nth-child(2) > table:nth-child(2) > tr > td').get()).strip()
            #remove ,state, country
            adItem['location'] = location_raw.split(",")[0]
            price_raw = item.css(
                'td:nth-child(2) > table:nth-child(2) > tr:nth-child(3) > td > b::text').get()
            #remove USD
            adItem['price'] = price_raw.split(" ")[0]
            yield adItem
