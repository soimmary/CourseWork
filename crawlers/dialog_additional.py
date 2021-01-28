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


# Парсим pdf
def parse_pdf(path):
    pdf_document = path
    doc = fitz.open(pdf_document)
    text = ''
    for current_page in range(len(doc)):
        page = doc.loadPage(current_page)
        page_text = page.getText("text")
        text += page_text
    return text


# Скачиваем pdf
def downloading_pdf(block):
        url = block['link']
        filename = block['path'][:-3]+'pdf'
        path = f'/Users/mariabocharova/PycharmProjects/Thesis/texts/pdfs/{filename}'
        urllib.request.urlretrieve(url, path)
        return path


# Записываем в таблицу metagata.csv
def write_to_metadata(path_file, title, author, date, resource):
    with open("/Users/mariabocharova/PycharmProjects/Thesis/metadata.csv", 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        a = [path_file, title, author, date, resource]
        file_writer.writerow(a)


# Записываем txt в папку Диалог 2004-2020
def write_to_txt(path, text):
    with open(f'/texts/Диалог_online/2018/{path}', 'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


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


def dialog_dictionary(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    info = soup.find_all('article', {'class': 'article-link'})
    resource = 'Итоги конференции «Диалог». ' + str(soup.find('h1', {'class': 'page-title-text'}))
    date = resource.split()[-1]
    for elem in info:
        try:
            block = {}
            author = re.findall(r'author">(.+?)</div>', str(elem), flags=re.DOTALL)[0]
            link = 'http://www.dialog-21.ru' + re.findall(r'a href="(.+?)"', str(elem))[0]
            title = re.findall(r'blank">(.+?)<', str(elem))[0]

            # Путь к файлу
            path = ''.join(random.choice(alphabet_num) for x in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(12)) + '.txt'
            if link.endswith('pdf'):
                block['link'] = link
            else:
                continue
            block = {'title': title.replace('\n', ' '),
                     'author': author.replace('\n', ' '),
                     'date': date.replace('\n', ' '),
                     'resource': resource, 'path': path,
                     'text': parse_pdf(downloading_pdf(block))}
            # Записываю в таблицу metadata.csv
            write_to_metadata(block['path'], block['title'],
                              block['author'], block['date'], block['resource'])
            # Записываю в папку
            write_to_txt(block['path'], block['text'])
        except Exception as e:
            print(e)
            continue


for year in range(2003, 2020):
    dialog_dictionary(f'http://www.dialog-21.ru/digest/{year}/online/')

