import fitz
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import random
import urllib.request


alphabet_num = '0123456789abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


# Имена всех существующих файлов в папке texts
def get_names():
    with open('/Users/mariabocharova/PycharmProjects'
          '/Thesis/metadata.csv', encoding='utf-8') as f:
        table = f.readlines()
        names = []
        for path in table:
            if path.split(';')[0] != '\n':
                names.append(path.split(';')[0])
    return names


# Работаю с данным из Диалога
blocks = []


def dialog_dictionary(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    info = soup.find_all('article', {'class': 'article-link'})

    resource = 'Итоги конференции «Диалог». ' + soup.find('h1', {'class': 'page-title-text'}).text
    date = resource.split()[-1]

    for elem in info:
        block = {}
        author = re.findall(r'author">(.+?)</div>', str(elem), flags=re.DOTALL)[0]
        link = 'http://www.dialog-21.ru' + re.findall(r'a href="(.+?)"', str(elem))[0]
        title = re.findall(r'blank">(.+?)<', str(elem))[0]

        # Путь к файлу
        path = ''.join(random.choice(alphabet_num) for x
                   in range(12)) + '.txt'
        while path in get_names():
            path = ''.join(random.choice(alphabet_num)
                           for x in range(12)) + '.txt'
        block['path'] = path
        block['title'] = title
        block['author'] = author
        block['date'] = date
        block['resource'] = resource
        block['link'] = link
        blocks.append(block)


for year in range(2003, 2021):
    dialog_dictionary(f'http://www.dialog-21.ru/digest/{year}/articles/')


# Скачиваем pdf
for block in blocks:
    url = block['link']
    filename = block['path'][:-3]+'pdf'
    urllib.request.urlretrieve(url, f'/Users/mariabocharova/PycharmProjects'
                                    f'/Thesis/texts/pdfs/{filename}')



# Парсим pdf
"""
def parse_pdf(path):
    pdf_document = path
    doc = fitz.open(pdf_document)
    for current_page in range(len(doc)):
        page = doc.loadPage(current_page)
        page_text = page.getText("text")
        print(page_text)
"""

