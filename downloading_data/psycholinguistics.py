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


# Записываем txt в папку
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/psycholinguistics/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Ссылки на выпуски (переадресация)
def get_links_1(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    other_links_raw = soup.find_all('a', href=re.compile('//iling-ran\.ru/web/news/\d{1,}_vpl'))
    other_links = ['https:'+re.findall('href="(.+?)"', str(j))[0] for j in other_links_raw]
    return other_links


# main_1
def get_dictionary_1(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    info = soup.find_all('li')
    for i in info:
        try:
            path = ''.join(random.choice(alphabet_num) for x
                           in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(13)) + '.txt'
            author = re.findall('<b>(.+?)</b>', str(i))[0]
            link = 'https:'+re.findall('<a href="(.+?)"', str(i))[0]
            title = re.findall('"_blank">(.+?)<', str(i))[0]
            resource = soup.find('title').text
            resource = re.findall('«.+', resource)[0]
            date = re.findall('\d\d\d\d', resource)[0]
            block = {'link': link, 'path': path,
                     'title': title, 'author': author, 'date': date,
                     'resource': resource}
            block['text'] = parse_pdf(downloading_pdf(block))
            # Записываю в таблицу metadata.csv
            write_to_metadata(block['path'], block['title'],
                              block['author'], block['date'], block['resource'])
            # Записываю в папку
            write_to_txt(block['path'], block['text'])
        except Exception as e:
            print(e)
            continue


# Ссылки на выпуски в формате pdf
def get_dictionary_2(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'utf-8'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    pdf_links_raw = soup.find_all('a', {'target': '_blank'},
                                  href=re.compile('//iling-ran\.ru/library/voprosy/\d{1,}\.pdf'))[:30]
    pdf_links = ['https:' + re.findall('href="(.+?)"', str(i))[0] for i in pdf_links_raw]
    titles = [re.findall('"_blank">(.+?)<', str(i))[0] for i in pdf_links_raw]
    dates = [re.findall('\d\d\d\d', str(i))[0] for i in pdf_links_raw]
    for elem in range(len(pdf_links_raw)):
        try:
            path = ''.join(random.choice(alphabet_num) for x
                           in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(13)) + '.txt'
            author = '-'
            link = pdf_links[elem]
            title = titles[elem]
            resource = title
            date = dates[elem]
            block = {'link': link, 'path': path,
                     'title': title, 'author': author, 'date': date,
                     'resource': resource}
            block['text'] = parse_pdf(downloading_pdf(block))
            # Записываю в таблицу metadata.csv
            write_to_metadata(block['path'], block['title'],
                              block['author'], block['date'], block['resource'])
            # Записываю в папку
            write_to_txt(block['path'], block['text'])
        except Exception as e:
            print(e)
            continue


get_dictionary_2('https://iling-ran.ru/web/ru/publications/journals/vpl')


"""for link in get_links_1('https://iling-ran.ru/web/ru/publications/journals/vpl'):
    get_dictionary_1(link)"""
