# pyenv install 3.7.7
# pyenv local 3.7.7
# pipenv -python 3.7.7
# pipenv install requests-html
# pipenv shell
# scrapy startproject <project>
# scrapy crawl <project>
# scrapy shell <url>

import scrapy
from ..items import ClassifiedscraperItem
import logging
from w3lib.html import remove_tags
import re
import furl


class FacebookSpider(scrapy.Spider):
    name = "facebook"

    def __init__(self, urls_file):
        self.urls_file = urls_file

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            urls_file=crawler.settings.get('FACEBOOK_URLS_FILE')
        )

    def start_requests(self):

        logging.info("url file: %s", self.urls_file)

        with open(self.urls_file, "rt") as f:
          start_urls = [url.strip() for url in f.readlines()]

         #dont_filter bypasses the duplicate url filter
        for url in start_urls:
            yield scrapy.Request(url=url, meta={'dont_redirect': True}, callback=self.parse, dont_filter=True)
            #yield SeleniumRequest(url=url, meta={'dont_redirect': True}, callback=self.parse)

    def parse(self, response):
        
        for item in response.xpath("//a[contains(@href, '/marketplace/item/')]/../../.."):
            #find the links to items
            #self.logger.info("Found:", item)
            adItem = ClassifiedscraperItem()
            adItem.set_all(None)
            adItem['source'] = self.name
            #response.request.url
            request_url_base = furl.furl(response.request.url).origin
            link_raw = item.xpath(
                ".//a[contains(@href, '/marketplace/item/')]/@href").get()
            link_raw = furl.furl(link_raw).remove(
                args=True, fragment=True).url
            adItem['link'] = request_url_base + link_raw
            adItem['price'] = remove_tags(item.xpath(".//span[starts-with(text(), '$')]").get())
            title_raw = remove_tags(item.get())

            adItem['title'] = re.sub("^\$\d+", "", title_raw)

            image_link_raw = item.css('img').xpath('@src').get()
            #image_link_raw = furl.furl(image_link_raw).remove(args=True,fragment=True).url
            adItem['image_link'] = image_link_raw

            yield adItem
