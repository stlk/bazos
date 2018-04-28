import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from bazos.spiders.bazos import BazosSpiderXPath

import config

import logging
import http.client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.ERROR)
requests_log.propagate = True

handler = SentryHandler(config.RAVEN_DSN)
handler.setLevel(logging.ERROR)

setup_logging(handler)

import verification
if verification.verify():
    print('Ověřeno')

    process = CrawlerProcess(get_project_settings())

    process.crawl(BazosSpiderXPath)
    result = process.start() # the script will block here until the crawling is finished

else:
    print('Ověření nebylo úspešné')
