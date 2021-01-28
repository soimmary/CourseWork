from bs4 import BeautifulSoup
import requests
import re
import time


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


url_part = 'https://www.dissercat.com/catalog/filologicheskie-nauki/yazykoznanie/'
for link, page in link_pages.items():
    get_links(url_part + link, page)
