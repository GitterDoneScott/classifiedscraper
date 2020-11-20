# pyenv install 3.7.7
# pyenv local 3.7.7
# pipenv -python 3.7.7
# pipenv install requests-html
# pipenv shell
# scrapy startproject <project>
# scrapy crawl ebay
# scrapy shell ""

import scrapy
from ..items import ClassifiedscraperItem
import logging
import json


class EbaySpider(scrapy.Spider):
    name = "ebay"

    def __init__(self, urls_file, ebay_app_id):
        self.urls_file = urls_file
        self.ebay_app_id = ebay_app_id

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            urls_file=crawler.settings.get('EBAY_URLS_FILE'),
            ebay_app_id=crawler.settings.get('EBAY_APP_ID')
        )

    def start_requests(self):

        logging.info("url file: %s", self.urls_file)

        with open(self.urls_file, "rt") as f:
          start_urls = [url.strip() for url in f.readlines()]

        headers = {'X-EBAY-SOA-SECURITY-APPNAME': self.ebay_app_id,
                   'X-EBAY-SOA-RESPONSE-DATA-FORMAT': 'JSON',
                   'X-EBAY-SOA-OPERATION-NAME': 'findItemsByKeywords',
                   }

        for url in start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        
        resp = json.loads(response.body)


        try:
            listings = resp['findItemsByKeywordsResponse'][0]['searchResult'][0]['item']

            for listing in listings:
            
                adItem = ClassifiedscraperItem()
                adItem.set_all(None)
                adItem['source'] = self.name
                adItem['source_link'] = resp['findItemsByKeywordsResponse'][0]['itemSearchURL'][0]
                adItem['title'] = listing['title'][0]
                adItem['link'] = listing['viewItemURL'][0]
                adItem['image_link'] = listing['galleryURL'][0]
                adItem['location'] = listing['location'][0]
                adItem['price'] = listing['sellingStatus'][0]['currentPrice'][0]['__value__']
                yield adItem
        except:
            self.logger.info("ERROR:", str(resp))

    def parse_json_recursively(json_input, lookup_key):
        if isinstance(json_input, dict):
            for k, v in json_input.items():
                if k == lookup_key:
                    yield v
                else:
                    yield from parse_json_recursively(v, lookup_key)
        elif isinstance(json_input, list):
            for item in json_input:
                yield from parse_json_recursively(item, lookup_key)

