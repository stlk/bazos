import requests
import config
import pickle

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

def load_cookies():
    with open('session.pickle', 'rb') as f:
        session.cookies = pickle.load(f)

def save_cookies():
    with open('session.pickle', 'wb') as f:
        pickle.dump(session.cookies, f)

def needs_verification():
    response = session.get('https://auto.bazos.cz/pridat-inzerat.php')

    needs_verification_index = response.text.find('Před přidáním inzerátu je nutné ověření mobilního telefonu')

    return needs_verification_index >= 0

def verify():
    try:
        load_cookies()
    except Exception as e:
        print('Nepodařilo se obnovit session, bude nutné ověření SMS.')
        pass

    if needs_verification():
        raise Exception('Needs SMS verification!')

    payload = {
        'podminky': '1',
        'teloverit': config.PHONE_VERIFICATION,
        'Submit': 'Odeslat',
    }

    response = session.post('https://auto.bazos.cz/pridat-inzerat.php', data=payload)

    input_index = response.text.find('name="klic" id="klic"')

    if input_index == -1:
        print('Ověření není nutné')
        return True

    klic = input('Zadejte prosim Mobilní klíč: ')

    payload = {
        'klic': klic,
        'klictelefon': f'+420{config.PHONE_VERIFICATION}',
        'Submit': 'Odeslat',
    }

    response = session.post('https://auto.bazos.cz/pridat-inzerat.php', data=payload)

    print(response.text)

    if response.text.find('Chybně zadaný mobilní klíč') > 0:
        print('Chybně zadaný mobilní klíč')
        return False

    save_cookies()

    return session.cookies['bkod']
