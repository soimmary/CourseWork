import fitz
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re
import csv
import random
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
    filename = block['path'][:-3] + 'pdf'
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


# Записываем txt
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/linguisics_and_language_teaching/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Ссылки на выпуски
def get_links(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'cp1251'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    links_raw = soup.find_all('a', href=re.compile('//iling-ran\.ru/library/sborniki/for_lang/.+\.htm'))
    all_links = ['https:' + re.findall('href="(.+?)"', str(i))[0] for i in links_raw]
    return all_links


# Ссылки на выпуски в формате pdf
def make_file(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'cp1251'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    info_raw = soup.find_all('a', href=re.compile('\.pdf'))
    pdf_links = [url[:-9] + re.findall('href="(.+?)"', str(i))[0] for i in info_raw]
    dates = [re.findall('\d\d\d\d', str(i))[0] for i in pdf_links]
    issues = [re.findall('\d\d\d\d_(\d\d?)', str(i))[0] for i in pdf_links]
    info = [re.findall('">(.+?)<.a>',
                       str(i).replace('\n', ' ').replace('\r', ''))[0]
            for i in info_raw]
    for i in range(len(pdf_links)):
        try:
            path = ''.join(random.choice(alphabet_num) for x
                           in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(13)) + '.txt'
            date = dates[i]
            line = re.sub('<.+?>', ' ', info[i]).strip()
            possible_author = re.findall('[А-ЯЁA-Z]\. ?[А-ЯЁA-Z]\. ?[А-ЯЁа-яё]+\.', line)
            if len(possible_author) == 1:
                author = possible_author[0]
            else:
                author = '-'
            link = pdf_links[i]
            resource = f'«Лингвистика и методика преподавания иностранных языков. ' \
                       f'{dates[i]}. №{issues[i]}»'
            title = re.sub('[А-ЯЁA-Z]\. ?[А-ЯЁA-Z]\. ?[А-ЯЁа-яё]+\.', '', line)[3:].strip()
            if int(date.strip()) > 2010:
                title = resource
            if len(title) == 0:
                title = '-'
            block = {'link': link, 'path': path,
                     'title': title, 'author': author,
                     'date': date, 'resource': resource}
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
def make_file_2(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    req.encoding = 'cp1251'
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    info_raw = soup.find_all('a', href=re.compile('\.pdf'))
    pdf_links = [re.findall('href="(.+?)"', str(i))[0] for i in info_raw]
    for i in range(len(pdf_links)):
        try:
            path = ''.join(random.choice(alphabet_num) for x
                           in range(12)) + '.txt'
            while path in get_names():
                path = ''.join(random.choice(alphabet_num)
                               for x in range(13)) + '.txt'
            link = pdf_links[i]
            date = re.findall('\d{4}', link)[0]
            issue = re.findall('\d{4}_(\d\d?)', link)[0]
            title = f'«Лингвистика и методика преподавания иностранных языков. ' \
                    f'{date}. №{issue}»'
            resource = title
            author = '-'
            block = {'link': link, 'path': path,
                     'title': title, 'author': author,
                     'date': date, 'resource': resource}
            block['text'] = parse_pdf(downloading_pdf(block))
            # Записываю в таблицу metadata.csv
            write_to_metadata(block['path'], block['title'],
                              block['author'], block['date'], block['resource'])
            # Записываю в папку
            write_to_txt(block['path'], block['text'])
        except Exception as e:
            print(e)
            continue


for elem in get_links('https://iling-ran.ru/web/ru/publications/for_lang')[0:2]:
    make_file(elem)

for elem in get_links('https://iling-ran.ru/web/ru/publications/for_lang')[2:]:
    make_file_2(elem)
