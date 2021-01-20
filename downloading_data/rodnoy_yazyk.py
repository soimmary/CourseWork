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
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    all_links = []
    info = soup.find_all('p', {'class': 'has-medium-font-size'})
    for i in info:
        all_links.append('http://rodyaz.ru'+re.findall('href="(.+?)"', str(i))[0])
    return all_links


# Скачиваю ссылку на pdf
def download_pdf_link(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    pdf_link = soup.find('a', href=re.compile('\.pdf')).attrs['href']
    return pdf_link


# Скачиваем pdf
def downloading_pdf(block):
    url = block['link']
    filename = block['path'][:-3]+'pdf'
    path = f'/Users/mariabocharova/PycharmProjects/Thesis/texts/pdfs/{filename}'
    with open(path, 'wb') as f:
        f.write(requests.get(url).content)
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


# Записываем txt в папку Диалог 2004-2020
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/rodnoy_yazyk/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# main
def get_dictionary(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    info = soup.find_all('a', {'rel': 'noreferrer noopener'})
    for i in info:
        try:
            path = ''.join(random.choice(alphabet_num) for x
                           in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(13)) + '.txt'
            link_0 = re.findall('href="(.+?)"', str(i))[0]
            link = download_pdf_link(link_0)
            author = '-'
            title = re.findall('>(.+?)<', str(i))[0]
            date = re.findall('\d\d\d\d', url)[0]
            resource = '«Социолингвистика»'
            block = {'link': link, 'path': path,
                     'title': title, 'author': author, 'date': date,
                     'resource': resource}
            block['text'] = parse_pdf(downloading_pdf(block))
            # Записываю в таблицу metadata.csv
            write_to_metadata(block['path'], block['title'],
                              block['author'], block['date'], block['resource'])
            # Записываю в папку
            write_to_txt(block['path'], block['text'])
        except Exception:
            continue


for i in get_links('http://sociolinguistics.ru/архив/'):
    get_dictionary(i)

# Далее вручную добавляю в таблицу имена авторов
