# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from shutil import copyfile
import verification
import config
import os

from scrapy.selector import Selector

def get_spam_protection(rubrika):
    response = verification.session.get(f'https://{rubrika}.bazos.cz/pridat-inzerat.php')
    selected = Selector(text = response.content).xpath('//form[@id="formpridani"]//input[@type="hidden"]')[0]
    return (selected.xpath('@name').extract_first(), selected.xpath('@value').extract_first())

def create_listing(data):
    print('Creating listing with data...')
    print(data)
    rubrika = data['rubrika']
    data.pop('rubrika')

    spam_protection_key, spam_protection_value = get_spam_protection(rubrika)
    payload = {
        spam_protection_key: spam_protection_value,
        'heslo': config.PASSWORD,
        'cenavyber': '1',
        'maili': '',
        'Submit': 'Odeslat',
    }
    payload.update(data)

    files = {}
    for idx in range(1, 10):
        index = idx - 1
        file_object = open('photos/' + data['files'][index]['path'], 'rb') if idx <= len(data['files']) else ''
        files['souborp{0}'.format('' if idx == 1 else idx)] = file_object

    payload.pop('file_urls')
    payload.pop('files')

    response = verification.session.post(f'https://{rubrika}.bazos.cz/insert.php', data=payload, files=files)

    for file_info in data['files']:
        os.remove('photos/' + file_info['path'])

    print(response.text)

    if response.text.find('Inzerát nebyl vložen') > -1:
        print('/n')
        print(f'Inzerát {data["nadpis"]} NEBYL vložen do bazaru.')
        return

    print(f'Inzerát {data["nadpis"]} byl vložen do bazaru.')

class BazosPipeline(object):
    def process_item(self, item, spider):
        for idx, image in enumerate(item['files']):
            image_path = image['path']
            copyfile(f'photos/{image_path}', f'backups/{item["id"]}/{idx}.jpg')

        create_listing(item)
        return item
