# pyenv install 3.7.7
# pyenv local 3.7.7
# pipenv -python 3.7.7
# pipenv install requests-html
# pipenv shell
# scrapy startproject <project>
# scrapy crawl facebook
# scrapy shell "https://greenville.craigslist.org/search/bia?query=Release+%7C+Roscoe+%7C+Fuse+%7C+Fluid+%7C+Stumpjumper+%7C+Spectral+%7C+Trance+%7C+Jeffsy+%7C+Timberjack+%7C+Meta+%7C+Origin&sort=rel&search_distance=150&postal=29681&min_price=999"

import scrapy
from scrapy.utils.markup import remove_tags
from ..items import ClassifiedscraperItem
import logging


class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def __init__(self, urls_file):
        self.urls_file = urls_file

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            urls_file=crawler.settings.get('CRAIGSLIST_URLS_FILE')
        )

    def start_requests(self):
        
        logging.info("url file: %s", self.urls_file)

        with open(self.urls_file, "rt") as f:
          start_urls = [url.strip() for url in f.readlines()]
        
         #dont_filter bypasses the duplicate url filter
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):

        for item in response.css('li.result-row'):
            #self.logger.info("Found:", item)
            adItem = ClassifiedscraperItem()
            adItem.set_all(None)
            adItem['title'] = item.css('a.result-title.hdrlnk::text').get(default='not-found')
            adItem['link'] = item.css(
                'a.result-title.hdrlnk::attr(href)').get(default='not-found')
            #sortable-results > ul > li:nth-child(1) > a > div.swipe > div > div:nth-child(1) > img
            #sortable-results > ul > li:nth-child(2) > a > img
            #// *[ @ id = "sortable-results"] / ul / li[1] / a / div[1] / div / div[1] / img
            #/html/body/section/form/div[4]/ul/li[1]/a/div[1]/div/div[1]/img
            #this is loaded by JS. Need to either render js or pull up ad
            adItem['image_link'] = item.css('img.hoverZoomLink::attr(src)').get(default='not-found')
            
            
            adItem['location'] = item.css('span.nearby::text').get(
                default='not-found')

            
            adItem['price'] = item.css(
                'span.result-price::text').get(default='not-found')
            
            #sortable-results > ul > li:nth-child(2) > div > span.result-meta > span.result-tags > span.maptag
            adItem['distance'] = item.css(
                'span.maptag::text').get(default='not-found')
            yield adItem
