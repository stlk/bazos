# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from shutil import copyfile
import verification
import config

def create_listing(data):
    payload = {
        'fsdsdfs': 'tertertaa',
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

    payload.pop('image')
    payload.pop('file_urls')
    payload.pop('files')

    response = verification.session.post('https://auto.bazos.cz/insert.php', data=payload, files=files)

    print(response.text)

    if response.text.find('Inzerát nebyl vložen do našeho bazaru') > -1:
        print('/n')
        print(f'Inzerát {data["nadpis"]} NEBYL vložen do bazaru.')

    print(f'Inzerát {data["nadpis"]} byl vložen do bazaru.')

class BazosPipeline(object):
    def process_item(self, item, spider):
        for idx, image in enumerate(item['files']):
            image_path = image['path']
            copyfile(f'photos/{image_path}', f'backups/{item["id"]}/{idx}.jpg')

        create_listing(item)
        return item
