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
from scrapy_splash import (
    SplashRequest,
    SlotPolicy,
)



class FacebookSpider(scrapy.Spider):
    name = "facebook"
    #override default user_agent header
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1'
    #2021-01-11 19:00:26 [root] DEBUG: response.request.headers: {b'User-Agent': [b'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'], b'Accept-Encoding': [b'gzip, deflate']}

    def __init__(self, urls_file):
        self.urls_file = urls_file

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            urls_file=crawler.settings.get('FACEBOOK_URLS_FILE')
        )

    def start_requests(self):

        logging.info("url file: " + self.urls_file)
 

        with open(self.urls_file, "rt") as f:
          start_urls = [url.strip() for url in f.readlines()]

        for url in start_urls:
            #import web_pdb; web_pdb.set_trace()
            yield scrapy.Request(url=url, meta = {'dont_redirect': True,'handle_httpstatus_list': [302]}, callback=self.parse)
            # yield SplashRequest(url, self.parse,
            #         args={
            #             # optional; parameters passed to Splash HTTP API
            #             'wait': 5,

            #             # 'url' is prefilled from request url
            #             # 'http_method' is set to 'POST' for POST requests
            #             # 'body' is set to request body for POST requests
            #         },
            #         #endpoint='render.html', # optional; default is render.html
            #         slot_policy=SlotPolicy.SINGLE_SLOT,  # optional
            #     )
 

    def parse(self, response):
        
        logging.debug("response.request.headers: " + str(response.request.headers))
        #logging.debug("response.request.body: " + str(response.request.body))
        logging.debug("response.headers: " + str(response.headers))
        #logging.debug("response.body: " + str(response.body))
        logging.debug("Title : " + str(response.xpath("//title/text()").extract_first(default='')))

        
        for item in response.xpath("//a[contains(@href, '/marketplace/item/')]/../../.."):
                
            logging.debug('item:' + str(item))
            #find the links to items
            adItem = ClassifiedscraperItem()
            adItem.set_all(None)
            adItem['source'] = self.name
            #response.request.url
            request_url_base = furl.furl(response.url).origin
            #request_url_base = 'https://www.facebook.com/'          
            
            link_raw = item.xpath( ".//a[contains(@href, '/marketplace/item/')]/@href").get()
            link_raw = furl.furl(link_raw).remove(args=True, fragment=True).url
            item_link = request_url_base + link_raw
            logging.debug('link:'+ item_link)
            adItem['link'] = item_link

            #price lives in a seperate span..lets hope it begins with a $
            item_price = remove_tags(item.xpath(".//span[starts-with(text(), '$')]").get())
            logging.debug('Price:' + item_price)
            adItem['price'] = item_price

            #concatenate the whole div tag...
            title_raw = remove_tags(item.xpath(".//img/@alt").get())
            logging.debug('title_raw:'  + title_raw)
            item_title = title_raw.split(' in ')[0]
            logging.debug('title:' + item_title)
            adItem['title'] = item_title

            item_location=title_raw.split(' in ')[1]
            logging.debug('location:' +item_location )
            adItem['location'] = item_location

            image_link_raw = remove_tags(item.xpath(".//img/@src").get())
            logging.debug('image_link_raw: ' + image_link_raw)
            adItem['image_link'] = image_link_raw
            
            yield adItem
        
        # for item in response.xpath("//a[contains(@href, '/marketplace/item/')]/../../.."):
            
        #     #find the links to items
        #     #self.logger.info("Found:", item)
        #     adItem = ClassifiedscraperItem()
        #     adItem.set_all(None)
        #     adItem['source'] = self.name
        #     #response.request.url
        #     request_url_base = furl.furl(response.request.url).origin
        #     link_raw = item.xpath(".//a[contains(@href, '/marketplace/item/')]/@href").get()
        #     link_raw = furl.furl(link_raw).remove(args=True, fragment=True).url
        #     adItem['link'] = request_url_base + link_raw
        #     #price lives in a seperate span..lets hope it begins with a $
        #     adItem['price'] = remove_tags(item.xpath(".//span[starts-with(text(), '$')]").get())
        #     #concatenate the whole div tag...
        #     title_raw = remove_tags(item.get())
        #     #remove leading non-alphabetic characters
        #     adItem['title'] = re.sub("^[^a-zA-Z]*", "", title_raw)
        #     image_link_raw = item.css('img').xpath('@src').get()
        #     #image_link_raw = furl.furl(image_link_raw).remove(args=True,fragment=True).url
        #     adItem['image_link'] = image_link_raw

        #     if adItem['link'] is not None:
        #       #pass the current adItem to the request if a detail link exists
        #       request = scrapy.Request(adItem['link'], callback=self.parse_detail_page)
        #       request.meta['adItem'] = adItem
        #       request.meta['dont_redirect']= True
        #       yield request
        #     yield adItem
    def parse_detail_page(self, response):
        
        #parse the ad detail page
        adItem = response.meta['adItem']
        #look for a div with the '·'
        raw_location_post_date = response.xpath(".//div[contains(text(), '·')]/text()").get()
        if raw_location_post_date is not None:
          adItem['location'] = raw_location_post_date.split('·')[0].strip()
          adItem['post_date'] = post_date_raw = raw_location_post_date.split('·')[1].strip()

        yield adItem
