# Scrapy settings for classifiedscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

#to be able to pull configuration from the environment
import os
#get project root
from scrapy.utils.conf import closest_scrapy_cfg

BOT_NAME = 'classifiedscraper'

SPIDER_MODULES = ['classifiedscraper.spiders']
NEWSPIDER_MODULE = 'classifiedscraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'classifiedscraper (+http://www.yourdomain.com)'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'classifiedscraper.middlewares.ClassifiedscraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'classifiedscraper.middlewares.ClassifiedscraperDownloaderMiddleware': 543,
#     'scrapy_selenium.SeleniumMiddleware': 800,
#}
    

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ITEM_PIPELINES = {
    'classifiedscraper.pipelines.KeywordFilterPipeline': 200,
    'classifiedscraper.pipelines.PersistancePipeline': 300,
    'classifiedscraper.pipelines.SendDiscordPipeline': 500,
}

DISCORD_NOTIFICATION_URL = os.getenv('SCRAPY_DISCORD_NOTIFICATION_URL', 'NOT FOUND')

PROJECT_ROOT = os.path.dirname(os.path.abspath(closest_scrapy_cfg()))

TINY_DB_FILE = os.path.join(PROJECT_ROOT, 'data', 'tiny_db.json')

CRAIGSLIST_URLS_FILE = os.path.join(PROJECT_ROOT, 'craigslist_urls.txt')
PINKBIKE_URLS_FILE = os.path.join(PROJECT_ROOT, 'pinkbike_urls.txt')
FACEBOOK_URLS_FILE = os.path.join(PROJECT_ROOT, 'facebook_urls.txt')


FILTER_KEYWORDS_FILE = os.path.join(PROJECT_ROOT, 'filter_keywords.txt')

