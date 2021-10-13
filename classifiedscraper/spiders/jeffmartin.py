# python -m venv <venv dir>
# . bin/activate
# scrapy startproject <project>
# scrapy crawl <>
# scrapy shell <>

import scrapy
from w3lib.html import remove_tags
from ..items import ClassifiedscraperItem
import logging
import re
import furl


class JeffMartinSpider(scrapy.Spider):
    name = "jeffmartin"

    def start_requests(self):

        start_urls = ['https://www.jeffmartinauctioneers.com/auctions']
        
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        
        for item in response.xpath("//div[@class='auction  ']"):
            logging.debug('item:' + str(item))
            location= item.xpath("normalize-space(.//button[contains(@class,'location-link')])").get()  
            logging.debug('Location:'+ str(location))  
            # filter non SC items
            if not ( bool(re.search('SC', location)) or bool(re.search('South Carolina', location)) ):
                logging.debug('SC NOT found: ')
                continue

            adItem = ClassifiedscraperItem()
            adItem.set_all(None)
            adItem['source'] = self.name
            adItem['location'] = location

            #response.request.url
            request_url_base = furl.furl(response.request.url).origin
            logging.debug('request_url_base:'+ request_url_base)
            link_raw = item.xpath(".//a/@href").get(default='/not-found')
            item_link = request_url_base + link_raw
            logging.debug('link:'+ item_link)
            adItem['link'] = item_link

            title_raw = remove_tags(item.xpath("normalize-space(.//p[@class='auctionTitle'])").get())
            logging.debug('title_raw:'  + title_raw)
            adItem['title'] = title_raw

            #image_link_raw = remove_tags(item.xpath(".//img/@src").get())
            #logging.debug('image_link_raw: ' + image_link_raw)
            #adItem['image_link'] = image_link_raw

            #raw_post_date = item.xpath("normalize-space(.//div[contains(@class,'auctionLocation')]/span)").get()
            #logging.debug('raw_post_date:'  + raw_post_date)
            #adItem['post_date'] = raw_post_date.split('ST')[0].strip()
            
            #raw_desc = item.xpath("normalize-space(.//div[@class='col-sm-12'])").get()
            #logging.debug('raw_post_date:'  + raw_post_date)
            #adItem['description'] = raw_desc
            
            yield adItem
    
