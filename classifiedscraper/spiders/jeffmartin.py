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
        
        for item in response.xpath("//*[@class='upcoming-item-a']"):
            location= item.xpath(".//span[contains(@class,'upcoming-info')]/text()").get()    
            # filter non SC items
            if not bool(re.search('SC', location)):
                #print('SC NOT found')
                continue

            adItem = ClassifiedscraperItem()
            adItem.set_all(None)
            adItem['source'] = self.name
            #response.request.url
            request_url_base = furl.furl(response.request.url).origin
            link_raw = item.xpath("./@href").get()
            adItem['link'] = request_url_base + link_raw
            adItem['title'] = item.xpath("normalize-space(.//span[@class='upcoming-title'])").get()
            adItem['location'] = location
            raw_post_date = item.xpath("normalize-space(.//span[contains(@class,'upcoming-date')])").get()
            adItem['post_date'] = raw_post_date.split('ST')[0].strip()
            adItem['description'] = item.xpath("normalize-space(.//div[@class='col-sm-12'])").get()
            


            yield adItem
    
