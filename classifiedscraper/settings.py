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
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

BOT_NAME = 'classifiedscraper'
LOG_LEVEL=os.getenv('CLASSIFIEDSCRAPER_LOG_LEVEL', 'ERROR')
LOG_STDOUT='True'
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
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
   'Connection:' : 'close',
#   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'en-us',
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 410,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 420,
    'classifiedscraper.middlewares.ClassifiedscraperDownloaderMiddleware': None,
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 450,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    'classifiedscraper.middlewares.HeaderDebugDownloadMiddleware':None,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

FAKEUSERAGENT_PROVIDERS = [
    # this is the first provider we'll try
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',
    # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FakerProvider',
    # fall back to USER_AGENT value
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',
]


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
AUTOTHROTTLE_TARGET_CONCURRENCY = .1
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

DISCORD_NOTIFICATION_URL = os.getenv('CLASSIFIEDSCRAPER_DISCORD_NOTIFICATION_URL', 'NOT FOUND')
EBAY_APP_ID = os.getenv('EBAY_APP_ID', 'NOT FOUND')

PROJECT_ROOT = os.path.dirname(os.path.abspath(closest_scrapy_cfg()))

TINY_DB_FILE = os.path.join(PROJECT_ROOT, 'data', 'tiny_db.json')

CRAIGSLIST_URLS_FILE = os.path.join(PROJECT_ROOT, 'craigslist_urls.txt')
PINKBIKE_URLS_FILE = os.path.join(PROJECT_ROOT, 'pinkbike_urls.txt')
FACEBOOK_URLS_FILE = os.path.join(PROJECT_ROOT, 'facebook_urls.txt')
EBAY_URLS_FILE = os.path.join(PROJECT_ROOT, 'ebay_urls.txt')


FILTER_KEYWORDS_FILE = os.path.join(PROJECT_ROOT, 'filter_keywords.txt')

#DOWNLOADER_CLIENT_TLS_CIPHERS='TLS_RSA_WITH_RC4_128_SHA'
#this seemed to fix the craigslist 403 issue...why?
DOWNLOADER_CLIENT_TLS_METHOD='TLSv1.2'
DOWNLOADER_CLIENT_TLS_VERBOSE_LOGGING=True

#pip install git+https://github.com/ly95/scrapy-headless.git
#pip install git+https://github.com/canada4663/scrapy-headless.git

# SELENIUM_GRID_URL = 'http://localhost:4444/wb/hub' 
# SELENIUM_NODES = 1  # Number of nodes(browsers) you are running on your grid
# SELENIUM_CAPABILITIES = DesiredCapabilities.FIREFOX

# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_headless.HeadlessDownloadHandler",
#     "https": "scrapy_headless.HeadlessDownloadHandler",
# }

SPLASH_URL = 'http://splash:8050'
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
