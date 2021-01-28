import fitz
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import csv
import random
import urllib.request
import time
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
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/voprosy_yaz/{path}',
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
    all_links = []
    info = soup.find_all('a', href=re.compile('/ru/archive/\d\d\d\d-\d\d?'))
    for i in info:
        links = re.findall(r'href="(.+?)"', str(i))[0]
        all_links.append('http://vja.ruslang.ru'+str(links))
    return all_links


# Создаем txt документ и пополняем таблицу
def make_file(url):
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
                           in range(13)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(12)) + '.txt'
            title = re.findall(r'hreflang="ru">(.*?)</a>', elem)[0]
            author = re.findall(r'<em>(.*?)</em>', elem)[0]
            date = re.findall(r'/ru/archive/(\d\d\d\d)', elem)[0]
            issue = re.findall(r'/ru/archive/\d\d\d\d-(\d)', elem)[0]
            resource = f'«Вопросы языкознания. {date}. №{issue}»'
            page_1 = re.findall(r'/ru/archive/\d\d\d\d-\d/(\d{1,})-\d{1,}', elem)[0]
            page_2 = re.findall(r'/ru/archive/\d\d\d\d-\d/\d{1,}-(\d{1,})', elem)[0]
            probable_pdf = f'http://vja.ruslang.ru/sites/default/files/articles/' \
                           f'{date}/{issue}/{date}-{issue}_{page_1}-{page_2}.pdf'
            if urllib.request.urlopen(probable_pdf).getcode() == 200:
                block = {'link': probable_pdf, 'path': path,
                         'title': title, 'author': author, 'date': date,
                         'resource': resource}
                block['text'] = parse_pdf(downloading_pdf(block))
                # Записываю в таблицу metadata.csv
                write_to_metadata(block['path'], block['title'],
                                  block['author'], block['date'], block['resource'])
                # Записываю в папку
                write_to_txt(block['path'], block['text'])
            else:
                return
        except Exception as e:
            print(e)
            continue


for elem in get_links('http://vja.ruslang.ru/ru/archive'):
    make_file(elem)
    time.sleep(1)
