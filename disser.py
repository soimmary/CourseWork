from bs4 import BeautifulSoup
import requests
import re
import csv
import string
import time


alphabet_num = string.ascii_letters + string.digits


# Записываем в таблицу metagata.csv
def write_to_metadata(path_file, title, author, date, resource):
    with open("/Users/mariabocharova/PycharmProjects/Thesis/metadata.csv", 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        a = [path_file, title, author, date, resource]
        file_writer.writerow(a)


# Записываем txt в папку
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/disser/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Все существующие имена документов
def get_names():
    with open('/Users/mariabocharova/PycharmProjects'
          '/Thesis/metadata.csv', encoding='utf-8') as f:
        table = f.readlines()
        names = set()
        for path in table:
            if path.split(';')[0] != '\n':
                names.add(path.split(';')[0])
    return names


link_pages = {'hrusskii-yazyk': 299,
              'hgermanskie-yazyki': 216,
              'hteoriya-yazyka': 186,
              'hsravnitelno-istoricheskoe-tipologicheskoe-i-sopostaviteln': 133,
              'hyazyki-narodov-rossiiskoi-federatsii-s-ukazaniem-konkretn': 60,
              'hromanskie-yazyki': 34,
              'hyazyki-narodov-zarubezhnykh-stran-azii-afriki-aborigenov-': 27,
              'hprikladnaya-i-matematicheskaya-lingvistika': 9,
              'hslavyanskie-yazyki-zapadnye-i-yuzhnye': 6,
              'htyurkskie-yazyki': 5,
              'hkavkazskie-yazyki': 5,
              'hklassicheskaya-filologiya-vizantiiskaya-i-novogrecheskaya': 6,
              'hfinno-ugorskie-i-samodiiskie-yazyki': 3,
              'hmongolskie-yazyki': 3,
              'hiranskie-yazyki': 3,
              'hbaltiiskie-yazyki': 2,
              'semitskie-yazyki': 2}


# Ссылки на диссертации
def get_links(url, page_num):
    for number in range(1, page_num):
        try:
            session = requests.session()
            known_proxy_ip = '144.217.101.245:3129'
            proxy = {'http': known_proxy_ip, 'https': known_proxy_ip}
            response = session.get(url + f'?page={number}', proxies=proxy)
            page = response.text
            soup = BeautifulSoup(page, 'html.parser')
            links = soup.find_all('a', href=re.compile(r'content'))
            for link in links:
                link = 'https://www.dissercat.com' + re.findall('href="(.+?)"', str(link))[0]
                with open('disser_link.txt', 'a', encoding='utf-8') as f:
                    f.write(link + '\n')
            time.sleep(30)
        except Exception as e:
            print(e)


pre_link = 'https://www.dissercat.com/catalog/filologicheskie-nauki/yazykoznanie/'
for link, page in link_pages.items():
    get_links(pre_link + link, page)