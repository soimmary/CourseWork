import fitz
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import csv
import random
import urllib.request


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


# Скачиваем pdf
def downloading_pdf(block):
        url = block['link']
        filename = block['path'][:-3]+'pdf'
        path = f'/Users/mariabocharova/PycharmProjects/Thesis/texts/pdfs/{filename}'
        urllib.request.urlretrieve(url, path)
        return path


alphabet_num = '0123456789abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


# Парсим pdf
def parse_pdf(path):
    pdf_document = path
    doc = fitz.open(pdf_document)
    text = ''
    for current_page in range(len(doc)):
        page = doc.loadPage(current_page)
        page_text = page.getText('text')
        text += page_text
    return text


# Записываем в таблицу metagata.csv
def write_to_metadata(path_file, title, author, date, resource):
    with open("/Users/mariabocharova/PycharmProjects/Thesis/metadata.csv", 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        a = [path_file, title, author, date, resource]
        file_writer.writerow(a)


# Записываем txt в папку
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/acta_linguistica/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Словарь с соответствием выпуска и года 2006-2020
year_issue = {}
for i, j in zip(range(2006, 2021), range(2, 17)):
    year_issue[f'Т. {j},'] = i


# Ссылки на выпуски ALP 2006-2017
def get_links(url):
    all_links = {}
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    info = soup.find_all('a', href=re.compile('\.pdf$'))
    for i in info:
        link = re.findall(r'href="(.+?)"', str(i))[0]
        issue = re.findall(r'tom">(.+?)<', str(i))[0]
        part = re.findall(r'part">(.+?)<', str(i))[0]
        date = year_issue[issue]
        all_links[link] = issue+' '+part+', '+str(date)
    return all_links


# main
def make_dictionary(url, info):
    block = {}
    path = ''.join(random.choice(alphabet_num) for x
                    in range(12)) + '.txt'
    while path in get_names():
        path = ''.join(random.choice(alphabet_num)
                        for x in range(12)) + '.txt'
    link = url
    title = 'Acta Linguistica Petropolitana, '+str(info)
    author = '–'
    date = info[-4:]
    resource = title

    block['link'] = link
    block['path'] = path
    block['title'] = title
    block['author'] = author
    block['date'] = date
    block['resource'] = resource
    block['text'] = parse_pdf(downloading_pdf(block))

    # Записываю в таблицу metadata.csv
    write_to_metadata(block['path'], block['title'],
                        block['author'], block['date'], block['resource'])
    # Записываю в папку
    write_to_txt(block['path'], block['text'])


"""for link, info in list(get_links('https://alp.iling.spb.ru/issues.ru.html').items()):
    make_dictionary(link, info)"""


### Вторая часть: парсинг 2018-2020 ###

# Ссылки на выпуски ALP 2006-2017
def get_links_2(url):
    all_links_2 = {}
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    links = soup.find_all('a', href=re.compile('[xiv]+\d\.ru\.html$'))
    for i in links:
        link = re.findall(r'href="(.+?)"', str(i))[0]
        issue = re.findall(r'tom">(.+?)<', str(i))[0]
        part = re.findall(r'part">(.+?)<', str(i))[0]
        date = year_issue[issue]
        all_links_2[link] = issue+' '+part+', '+str(date)
    return all_links_2


def make_dictionary_2(url, info):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    path = ''.join(random.choice(alphabet_num) for x
                   in range(12)) + '.txt'
    while path in get_names():
        path = ''.join(random.choice(alphabet_num)
                       for x in range(12)) + '.txt'
    link = soup.find('a', {'class': 'article-download-link'})['href']
    title = 'Acta Linguistica Petropolitana, ' + str(info)
    author = '–'
    date = info[-4:]
    resource = title

    block = {}
    block['link'] = link
    block['path'] = path
    block['title'] = title
    block['author'] = author
    block['date'] = date
    block['resource'] = resource
    block['text'] = parse_pdf(downloading_pdf(block))

    # Записываю в таблицу metadata.csv
    write_to_metadata(block['path'], block['title'],
                      block['author'], block['date'], block['resource'])
    # Записываю в папку
    write_to_txt(block['path'], block['text'])


for link, info in list(get_links_2('https://alp.iling.spb.ru/issues.ru.html').items()):
    make_dictionary_2(link, info)
