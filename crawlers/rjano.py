import fitz
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import csv
import random
import string
import urllib.request


alphabet_num = string.ascii_letters + string.digits


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


# Ссылки на выпуски
def get_links(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    all_links = []
    info = soup.find_all('div', {'class': 'nomer'})
    for i in info:
        links = ['http://rjano.ruslang.ru'+j for j in
                 re.findall(r'/ru/archive/\d\d\d\d-\d', str(i))]
        all_links.extend(links)
    return all_links


# Скачиваю ссылку на pdf
def download_pdf_link(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    pdf_link = soup.find('iframe').attrs['data-src']
    return pdf_link


# Скачиваем pdf
def downloading_pdf(block):
        url = block['link']
        filename = block['path'][:-3]+'pdf'
        path = f'/Users/mariabocharova/PycharmProjects/Thesis/texts/pdfs/{filename}'
        urllib.request.urlretrieve(url, path)
        return path


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
    with open("/Users/mariabocharova/PycharmProjects/Thesis/metadata.csv",
              'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        a = [path_file, title, author, date, resource]
        file_writer.writerow(a)


# Записываем txt в папку
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/РЯНО/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Создаем txt документ и пополняем таблицу
def meke_file(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    info = soup.find_all('td', {'class': 'views-field views-field-title table__cell'})
    for elem in info:
        elem = str(elem)
        try:
            path = ''.join(random.choice(alphabet_num) for x
                           in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(12)) + '.txt'
            link = 'http://rjano.ruslang.ru' + re.findall(r'a href="(.+?)"', elem)[0]
            title = re.findall(r'hreflang="ru">(.*?)</a>', elem)[0]
            author = re.findall(r'<em>(.*?)</em>', elem)[0]
            date = re.findall(r'/ru/archive/(\d\d\d\d)', elem)[0]
            issue = re.findall(r'/ru/archive/\d\d\d\d-(\d)', elem)[0]
            resource = f"«Русский язык в научном освещении. {date}. №{issue}»"
            block = {'link': download_pdf_link(link), 'path': path,
                     'title': title, 'author': author, 'date': date,
                     'resource': resource}
            block['text'] = parse_pdf(downloading_pdf(block))
            # Записываю в таблицу metadata.csv
            write_to_metadata(block['path'], block['title'],
                              block['author'], block['date'], block['resource'])
            # Записываю в папку "Диалог 2004-2020"
            write_to_txt(block['path'], block['text'])
        except Exception as e:
            print(e)
            continue


for elem in get_links('http://rjano.ruslang.ru/ru/archive'):
    make_file(elem)
