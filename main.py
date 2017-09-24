import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from bazos.spiders.bazos import ToScrapeSpiderXPath

# import logging
# import http.client
#
# http.client.HTTPConnection.debuglevel = 1
#
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


import verification
if verification.verify():
    print('Ověřeno')

    process = CrawlerProcess(get_project_settings())

    process.crawl(ToScrapeSpiderXPath)
    result = process.start() # the script will block here until the crawling is finished

else:
    print('Ověření nebylo úspešné')
