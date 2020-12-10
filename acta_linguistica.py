from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re


# Ссылки на выпуски ALP 2018-2020
def get_links(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    all_links = []
    info = soup.find_all('a', href=re.compile('\.pdf'))
    for i in info:
        links = [j for j in re.findall(r'href="(.+?)"', str(i))]
        all_links.extend(links)

    # В toms и parts вылезают кракозябры
    toms = []
    for i in info:
        tom = [j for j in re.findall(r'tom">(.+?)<', str(i))]
        toms.extend(tom)

    parts = []
    for i in info:
        part = [j for j in re.findall(r'part">(.+?)<', str(i))]
        parts.extend(part)

    return toms, parts


print(get_links('https://alp.iling.spb.ru/issues.ru.html'))
