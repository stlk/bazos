import os
import scrapy
import re

import config

listing_url = f'https://www.bazos.cz/moje-inzeraty.php?telefon={config.PHONE}'

def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))

class BazosSpiderXPath(scrapy.Spider):
    name = 'bazos'
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

        file_urls = response.xpath('//a[contains(@onmouseover, "return zobrazek")]/@href').extract()
        if not file_urls:
            file_urls = response.xpath('//img[@id="bobrazek"]/@src').extract()
        yield {
            'id': listing_id,
            'nadpis': response.xpath('//h1[@class="nadpis"]/text()').extract_first(),
            'popis': ''.join(response.xpath('//td/table/tr/td/div[@class="popis"]/text()').extract()),
            'jmeno': response.xpath('//td[@class="listadvlevo"]//a[contains(@href,"hodnoceni")]/text()').extract_first(),
            'telefoni': response.xpath('//td[@class="listadvlevo"]//a[contains(@href,"tel:")]/text()').extract_first(),
            'lokalita': get_num(response.xpath('//td[@class="listadvlevo"]//a[contains(@href,"maps")]/text()').re(r'\d{3}\s{1}\d{2}')[0]),
            'cena': get_num(response.xpath('//td[@class="listadvlevo"]//b/text()').extract_first()),
            'category': response.xpath('//link[@type="application/rss+xml"]/@href').re(r'(?<=cat=)\d+')[0],
            'rubrika': re.match(r'https:\/\/(\w+)\.', response.url).groups()[0],
            'file_urls': file_urls,
        }
