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


class PinkbikeSpider(scrapy.Spider):
    name = "pinkbike"

    def start_requests(self):
        urls = [
            'https://www.pinkbike.com/buysell/list/?lat=35.0693&lng=-82.4023&distance=73&q=title:%20%22Release%22%20OR%20%22Fluid%22%20OR%20%E2%80%9CStumpjumper%E2%80%9D%20OR%20%22%20Spectral%22%20OR%20%22Trance%22%20OR%20%22Jeffsy%22%20OR%20%22Timberjack%22%20OR%20%22Meta%E2%80%9D%20%20OR%20%E2%80%9COrigin%E2%80%9D&wheelsize=10'
        ]
        #dont_filter bypasses the duplicate url filter
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for item in response.css('div.bsitem > table  > tr > td:nth-child(2)'):
            #self.logger.info("Found:", item)
            adItem = ClassifiedscraperItem()
            adItem['title'] = item.css('div > a::text').get(default='not-found')
            adItem['link'] = item.css('div > a::attr(href)').get(default='not-found')
            location_raw = remove_tags(item.css('table:nth-child(2) > tr > td').get(default='not-found')).strip()
            #remove ,state, country
            adItem['location'] = location_raw.split(",")[0]
            price_raw = item.css('table:nth-child(2) > tr:nth-child(3) > td > b::text').get(default='not-found')
            #remove USD
            adItem['price'] = price_raw.split(" ")[0]
            yield adItem
