import fitz
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import csv
import random
import urllib.request
import string


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
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/onomastics/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Ссылки на выпуски
def get_links(url):
    ua = UserAgent(verify_ssl=False)
    headers = {'User-Agent': ua.random}
    session = requests.session()
    response = session.get(url, headers=headers)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    info = soup.find_all('ul', {'class': 'menu'})
    all_links = re.findall(r'href="(.+?)"', str(info))
    return all_links


# Создаем txt документ и пополняем таблицу
def make_file(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    info = soup.find_all('p')
    for elem in info:
        elem = str(elem)
        try:
            path = ''.join(random.choice(alphabet_num) for x
                           in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(12)) + '.txt'
            link = re.findall(r'a href="(.+?)"', elem)[0]
            link = re.findall(r'href="(.+?\.pdf)"', requests.get(link).text)[0]
            title = re.findall(r'>(.*?)</a>', elem)[0]
            title = re.sub(r'<.+?>', '', title)
            author = re.findall(r'<em>(.*?)</em>', elem)[0]
            date = re.findall(r'content/(\d\d\d\d)', elem)[0]
            resource = f"«Вопросы ономастики. {date}»"
            block = {'link': link, 'path': path,
                     'title': title, 'author': author, 'date': date,
                     'resource': resource, 'text': parse_pdf(downloading_pdf(block))}
            # Записываю в таблицу metadata.csv
            write_to_metadata(block['path'], block['title'],
                              block['author'], block['date'], block['resource'])
            # Записываю в папку
            write_to_txt(block['path'], block['text'])
        except IndexError:
            continue


for elem in get_links('http://www.onomastics.ru/content/voprosy-onomastiki'):
    make_file('http://www.onomastics.ru'+elem)
