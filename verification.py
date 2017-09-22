import requests
import config

session = requests.Session()

session.cookies.update({
    'btelefon': config.PHONE,
    'bjmeno': config.NAME,
    'bheslo': config.PASSWORD,
    'testcookie': 'ano',
})

session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
})

def verify():
    payload = {
        'podminky': '1',
        'teloverit': config.PHONE,
        'Submit': 'Odeslat',
    }

    response = session.post('https://auto.bazos.cz/pridat-inzerat.php', data=payload)

    input_index = response.text.find('name="klic" id="klic"')

    if input_index == -1:
        print('Neco se nepodarilo')
        return False

    klic = input('Zadejte prosim Mobilní klíč: ')

    payload = {
        'klic': klic,
        'klictelefon': f'+420{config.PHONE}',
        'Submit': 'Odeslat',
    }

    response = session.post('https://auto.bazos.cz/pridat-inzerat.php', data=payload)

    print(response.text)

    if response.text.find('Chybně zadaný mobilní klíč') > 0:
        print('Chybně zadaný mobilní klíč')
        return False

    return session.cookies['bkod']
