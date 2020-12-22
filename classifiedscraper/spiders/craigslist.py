# python -m venv <venv dir>
# . bin/activate
# scrapy startproject <project>
# scrapy crawl facebook
# scrapy shell "https://greenville.craigslist.org/search/bia?query=Release+%7C+Roscoe+%7C+Fuse+%7C+Fluid+%7C+Stumpjumper+%7C+Spectral+%7C+Trance+%7C+Jeffsy+%7C+Timberjack+%7C+Meta+%7C+Origin&sort=rel&search_distance=150&postal=29681&min_price=999"

import scrapy
from w3lib.html import remove_tags
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
        
        logging.info('url file: ', str(self.urls_file))

        with open(self.urls_file, "rt") as f:
          start_urls = [url.strip() for url in f.readlines()]
        
        # Set the headers here.
#         headers = {
#             'Host': 'greenville.craigslist.org',
#             'Connection': 'keep-alive',
# #            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
# #            'sec-ch-ua-mobile': '?0',
#             'Upgrade-Insecure-Requests': '1',
# #            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
#             'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0',
#  #           'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',

# #            'Sec-Fetch-Site': 'none',
# #            'Sec-Fetch-Mode': 'navigate',
# #            'Sec-Fetch-Dest': 'document',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'DNT' : '1',
#         }
        
        #dont_filter bypasses the duplicate url filter
        for url in start_urls:
         #   import pudb; pudb.set_trace()
            yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        
        for item in response.css('li.result-row'):
            #self.logger.info("Found:", item)
            adItem = ClassifiedscraperItem()
            adItem.set_all(None)
            adItem['source'] = self.name
            adItem['title'] = item.css('a.result-title.hdrlnk::text').get()
            adItem['link'] = item.css('a.result-title.hdrlnk::attr(href)').get()
            #sortable-results > ul > li:nth-child(1) > a > div.swipe > div > div:nth-child(1) > img
            #sortable-results > ul > li:nth-child(2) > a > img
            #// *[ @ id = "sortable-results"] / ul / li[1] / a / div[1] / div / div[1] / img
            #/html/body/section/form/div[4]/ul/li[1]/a/div[1]/div/div[1]/img
            #this is loaded by JS. Need to either render js or pull up ad
            #adItem['image_link'] = item.css('img.hoverZoomLink::attr(src)').get()
                 
            adItem['location'] = item.css('span.nearby::text').get()
   
            adItem['price'] = item.css(
                'span.result-price::text').get()
            
            #sortable-results > ul > li:nth-child(2) > div > span.result-meta > span.result-tags > span.maptag
            adItem['distance'] = item.css(
                'span.maptag::text').get()

            if adItem['link'] is not None:
                  #pass the current adItem to the request if a detail link exists
              request = scrapy.Request(adItem['link'], callback=self.parse_detail_page)
              request.meta['adItem'] = adItem
              yield request

            yield adItem
    
    def parse_detail_page(self, response):
        #parse the ad detail page
        adItem = response.meta['adItem']
        adItem['image_link'] = response.css('img[alt="1"]::attr(src)').get()
        
        yield adItem
