import fitz
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import csv
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


# Ссылки на выпуски
def get_links(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    all_links = []
    info = soup.find_all('a', href=re.compile('/istochnik_\d\d\d\d'))
    for i in info:
        links = ['http://www.ruslang.ru' + j for j in
                 re.findall(r'/istochnik_\d\d\d\d', str(i))]
        all_links.extend(links)
    return all_links


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
    with open("/Users/mariabocharova/PycharmProjects/Thesis/metadata.csv", 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        a = [path_file, title, author, date, resource]
        file_writer.writerow(a)


# Записываем txt в папку
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/Лингв_источниковедение/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


blocks = []


# main
def make_dictionary(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')

    names = soup.find_all('i')
    links_n_titles = soup.find_all('a', href=re.compile('/doc/lingistoch'))

    for i in range(len(names)):
        try:
            block = {}
            path = ''.join(random.choice(alphabet_num) for x
                           in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(12)) + '.txt'
            link = 'http://www.ruslang.ru' + re.findall(r'f="(.+?)">', str(links_n_titles[i]))[0]
            title = re.findall(r'>(.+?)</a>', str(links_n_titles[i]))[0]
            author = re.sub('<.+?>', '', str(names[i]))
            resource = re.sub('<.+?>', '', str(soup.find_all('h4')[0]))
            resource = resource.replace('\n', ' ')
            date = url[-4:]

            block['link'] = link
            block['path'] = path
            block['title'] = title
            block['author'] = author
            block['date'] = date
            block['resource'] = resource
            block['text'] = parse_pdf(downloading_pdf(block))
            blocks.append(block)

            # Записываю в таблицу metadata.csv
            write_to_metadata(block['path'], block['title'],
                              block['author'], block['date'], block['resource'])

            # Записываю в папку
            write_to_txt(block['path'], block['text'])
        except Exception as e:
            print(e)
            continue


for elem in get_links('http://www.ruslang.ru/istochnik'):
    make_dictionary(elem)

