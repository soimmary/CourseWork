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


# Записываем в таблицу metagata.csv
def write_to_metadata(path_file, title, author, date, resource):
    with open("/Users/mariabocharova/PycharmProjects/Thesis/metadata.csv",
              'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        a = [path_file, title, author, date, resource]
        file_writer.writerow(a)


# Записываем txt в папку
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/philology_portal/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Ссылки на выпуски
def get_links(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get('http://philology.ru/linguistics2.htm',
                      headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    urls = soup.find_all('a', href=re.compile(r'linguistics2.+\.htm'))
    all_links = []
    for i in urls:
        link = 'http://philology.ru/'+re.findall(r'href="(.+?)"', str(i))[0]
        if link not in all_links:
            all_links.append(link)
    return all_links


# Создаем txt документ и пополняем таблицу
def make_file(url):
    ua = UserAgent(verify_ssl=False)
    session = requests.session()
    req = session.get(url, headers={'User-Agent': ua.random})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    info = soup.find_all('p')
    path = ''.join(random.choice(alphabet_num) for x
                    in range(12)) + '.txt'
    while path in get_names():
        path = ''.join(random.choice(alphabet_num)
                        for x in range(12)) + '.txt'
    title = re.sub(r'<.+?>', '', str(info[1]))
    title = re.sub(r'\s\s+', ' ', title)
    author = re.sub(r'<.+?>', '', str(info[0]))
    resource = re.sub(r'<.+?>', '', str(info[2]))
    resource = re.sub(r'\s\s+', ' ', resource)
    date = re.findall(r'(\d\d\d\d)\.', str(info[2]))[0]
    text = soup.find('dd').text
    block = {'path': path, 'title': title,
             'author': author, 'date': date,
             'resource': resource, 'text': text}
    if len(block['date']) != 0:
        # Записываю в таблицу metadata.csv
        write_to_metadata(block['path'], block['title'],
                          block['author'], block['date'], block['resource'])
        # Записываю в папку
        write_to_txt(block['path'], block['text'])


for elem in get_links('http://philology.ru/linguistics2.htm'):
    try:
        make_file(elem)
    except Exception as e:
        print(e)
        continue
