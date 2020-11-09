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


class CraigslistSpider(scrapy.Spider):
    name = "craigslist"

    def start_requests(self):
        urls = [
            'https://greenville.craigslist.org/search/bia?query=Release+%7C+Fluid+%7C+Stumpjumper+%7C+Spectral+%7C+Trance+%7C+Jeffsy+%7C+Timberjack+%7C+Meta+%7C+Origin&sort=rel&search_distance=150&postal=29681&min_price=999'
        ]
        #dont_filter bypasses the duplicate url filter
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for item in response.css('div.result-info'):
            #self.logger.info("Found:", item)
            adItem = ClassifiedscraperItem()
            adItem['title'] = item.css('h3.result-heading > a::text').get(default='not-found')
            adItem['link'] = item.css('h3.result-heading > a::attr(href)').get(default='not-found')
            adItem['location'] = item.css('span.nearby::attr(title)').get(
                default='not-found')
            adItem['price'] = item.css(
                'span.result-price::text').get(default='not-found')
            yield adItem
