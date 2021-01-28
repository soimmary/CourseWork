from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import csv
import random
import string
import time


alphabet_num = string.ascii_letters + string.digits


# Записываем в таблицу metagata.csv
def write_to_metadata(path_file, title, author, date, resource):
    with open("/Users/mariabocharova/PycharmProjects/Thesis/metadata.csv", 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        a = [path_file, title, author, date, resource]
        file_writer.writerow(a)


# Записываем txt в папку
def write_to_txt(path, text):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/disser_selenium/{path}',
              'w', encoding='utf-8') as file:
        text = text.replace('\n', ' ')
        file.write(text)


# Все существующие имена документов
def get_names():
    with open('/Users/mariabocharova/PycharmProjects/'
              'Thesis/metadata.csv', encoding='utf-8') as f:
        table = f.readlines()
        names = set()
        for path in table:
            if path.split(';')[0] != '\n':
                names.add(path.split(';')[0])
    return names


# Путь до файла
def get_path():
    path = ''.join(random.choice(alphabet_num) for x
                   in range(12)) + '.txt'
    while path in get_names():
        path = ''.join(random.choice(alphabet_num)
                       for x in range(13)) + '.txt'
    return path


def get_text(url):
    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    driver = webdriver.Chrome(options=options,
                              executable_path=r'/Users/mariabocharova/PycharmProjects/'
                                              r'Thesis/downloading_data/chromedriver')
    driver.get(url)
    try:
        text_elem = driver.find_elements_by_class_name('doc-part')
        text = ''.join([i.text.replace('\n', '').strip() for i in text_elem])
        author = driver.find_element_by_xpath("//span[@itemprop='author']").text
        date = driver.find_element_by_xpath("//span[@itemprop='datePublished']").text
        title = driver.find_element_by_xpath("//b[@itemprop='name']").text
        resource = 'Электронная библиотека диссертаций'
        path = get_path()
        block = {'path': path, 'title': title,
                 'author': author, 'date': date,
                 'resource': resource, 'text': text}
        driver.close()
    except Exception as e:
        print(e)
        return
    # Записываю в таблицу metadata.csv
    write_to_metadata(block['path'], block['title'],
                      block['author'], block['date'], block['resource'])
    # Записываю в папку
    write_to_txt(block['path'], block['text'])


with open('disser_link.txt', 'r', encoding='utf-8') as file:
    for link in file.readlines()[12012:]:
        get_text(link.strip())
        #time.sleep(1)
