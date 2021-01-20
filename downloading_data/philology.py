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
        names = set()
        for path in table:
            if path.split(';')[0] != '\n':
                names.add(path.split(';')[0])
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
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/philology/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Ссылки на выпуски
def get_links(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    all_links = {}
    info = soup.find_all('a', href=re.compile('\.pdf'))
    for i in info:
        if int(re.findall(r'\((.+)\)', str(i))[0]) in range(1, 7):
            year = '2016'
        elif int(re.findall(r'\((.+)\)', str(i))[0]) in range(7, 13):
            year = '2017'
        elif int(re.findall(r'\((.+)\)', str(i))[0]) in range(13, 19):
            year = '2018'
        elif int(re.findall(r'\((.+)\)', str(i))[0]) in range(19, 25):
            year = '2019'
        elif int(re.findall(r'\((.+)\)', str(i))[0]) in range(25, 31):
            year = '2020'

        all_links['http://sciphilology.ru'+
                  re.findall(r'href="(.+?)"', str(i))[0]] = re.findall(r'>(.+?)<', str(i))[0]\
                                                            +', '+year
    return all_links


# main
def make_dictionary(url, info):

    path = ''.join(random.choice(alphabet_num) for x
                    in range(12)) + '.txt'
    while path in get_names():
        path = ''.join(random.choice(alphabet_num)
                        for x in range(12)) + '.txt'
    link = url
    title = info
    author = '–'
    date = info[-4:]
    resource = title

    block = {'link': link, 'path': path,
             'title': title, 'author': author,
             'date': date, 'resource': resource}
    block['text'] = parse_pdf(downloading_pdf(block))

    # Записываю в таблицу metadata.csv
    write_to_metadata(block['path'], block['title'],
                        block['author'], block['date'], block['resource'])
    # Записываю в папку
    write_to_txt(block['path'], block['text'])


for link, info in list(get_links('http://sciphilology.ru/archives').items()):
    make_dictionary(link, info)
