import os
import scrapy

import config

listing_url = f'https://www.bazos.cz/moje-inzeraty.php?telefon={config.PHONE}'

def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        listing_url,
    ]

    def parse(self, response):
        for item in response.xpath('//span[@class="vypis"]//table'):
            detail_url = item.xpath('.//span[@class="nadpis"]/a/@href').extract_first()
            if detail_url is not None:
                yield scrapy.Request(response.urljoin(detail_url), self.parse_detail)

    def parse_detail(self, response):
        listing_id = response.xpath('//meta[@name="description"]/@content').re(r'Inzerát č. (\d*):')[0]
        if not os.path.exists(f'backups/{listing_id}/'):
            os.makedirs(f'backups/{listing_id}/')
        with open(f'backups/{listing_id}/index.html', 'wb') as f:
            f.write(response.body)
        yield {
            'id': listing_id,
            'nadpis': response.xpath('//h1[@class="nadpis"]/text()').extract_first(),
            'popis': ''.join(response.xpath('//div[@class="popis"]/text()').extract()),
            'jmeno': response.xpath('//td[@class="listadvlevo"]//a[contains(@href,"hodnoceni")]/text()').extract_first(),
            'telefoni': response.xpath('//td[@class="listadvlevo"]//a[contains(@href,"tel:")]/text()').extract_first(),
            'lokalita': get_num(response.xpath('//td[@class="listadvlevo"]//a[contains(@href,"maps")]/text()').extract_first()),
            'cena': get_num(response.xpath('//td[@class="listadvlevo"]//b/text()').extract_first()),
            'category': response.xpath('//link[@type="application/rss+xml"]/@href').re(r'(?<=cat=)\d+')[0],
            'image': response.xpath('//img[@id="bobrazek"]/@src').extract_first(),
            'file_urls': response.xpath('//a[contains(@onmouseover, "return zobrazek")]/@href').extract(),
        }