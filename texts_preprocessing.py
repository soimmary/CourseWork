from tqdm import tqdm
import gensim
import logging
from razdel import sentenize
import csv
import os
import re


"""
Создаю txt документы, в которых все тексты по дате
"""


def make_docs_by_year():
    with open('/Users/mariabocharova/PycharmProjects/Thesis/new_metadata.csv',
              encoding='utf-8') as csvfile:
        table = csv.reader(csvfile, delimiter=';')
        header = next(table)
        for row in tqdm(table):
            name = row[0]
            year = row[3]
            if int(year) >= 1965:
                insert_text(get_text(name), year)


def get_text(name):
    try:
        with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/articles/{name}') as f1:
            text = f1.read()
    except FileNotFoundError:
        with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts/disser/{name}') as f2:
            text = f2.read()
    return text


def insert_text(text, year):
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/texts_by_year/{year}.txt', 'a') as f:
        f.write(text)


make_docs_by_year()

"""
Разбиваю тексты на предложения и лемматизирую
"""


path = '/Users/mariabocharova/PycharmProjects/Thesis/texts_by_year'
mystem_path = '/Users/mariabocharova/Desktop/mystem'


def break_by_sent(doc_path):
    global path
    with open(f'{path}/{doc_path}', 'r', encoding='utf-8') as f1:
        text = re.sub('\n', ' ', f1.read())
        # Удаляем переносы
        text = text.replace('­ ', '').replace('- ', '')
    with open(f'{path}/texts_by_year_sent/{doc_path[:-4]}_sent.txt', 'a', encoding='utf-8') as f2:
        for sent in list(sentenize(text)):
            f2.write(list(sent)[2])
            f2.write('\n')


for doc in tqdm(os.listdir(path)):
    if doc.endswith('txt'):
        break_by_sent(doc)


def lemmatizing_texts(doc):
    global mystem_path
    os.system(f'{mystem_path} '
              f'-wldcs '
              f'/Users/mariabocharova/PycharmProjects/Thesis/texts_by_year/texts_by_year_sent/{doc} '
              f'/Users/mariabocharova/PycharmProjects/Thesis/texts_by_year/texts_by_year_lemm/{doc[:4]}_lemm.txt')


for doc_by_sent in tqdm(os.listdir(f'{path}/texts_by_year_sent')):
    if doc_by_sent.endswith('_sent.txt'):
        print(doc_by_sent)
        lemmatizing_texts(doc_by_sent)


# Приводим тексты к красоте: заменяется \n\n+ на \n, удаляем {}
def cleaning(doc_path):
    global path
    with open(f'{path}/texts_by_year_lemm/{doc_path}', 'r') as f1:
        text = re.sub(r'[^а-яёА-ЯЁ\n]+', ' ', f1.read())
    with open(f'{path}/texts_by_year_lemm/{doc_path}', 'w') as f2:
        f2.write(text)


for doc_lemm in tqdm(os.listdir(f'{path}/texts_by_year_lemm')):
    if doc_lemm.endswith('_lemm.txt'):
        cleaning(doc_lemm)


# Создаю один ограмный txt со всеми данными
def make_one_txt(doc_path):
    with open(f'{path}/texts_by_year_lemm/{doc_path}', 'r', encoding='utf-8') as f1:
        text = f1.read()
    with open(f'/Users/mariabocharova/PycharmProjects/Thesis/string_corpora.txt',
              'a', encoding='utf-8') as f2:
        f2.write(text)


for elem in tqdm(os.listdir(f'{path}/texts_by_year_lemm')):
    if elem.endswith('_lemm.txt'):
        make_one_txt(elem)


# Создаю модель
def create_w2v_model():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus = '/Users/mariabocharova/PycharmProjects/Thesis/string_corpora.txt'
    data = gensim.models.word2vec.LineSentence(corpus)
    model = gensim.models.Word2Vec(data, size=500, window=10, min_count=2, sg=0)
    model.save("ling_corpora_word2vec.model")


model = gensim.models.Word2Vec.load("ling_corpora_word2vec.model")
for word in model.wv.most_similar('палатализация', topn=100):
    print(word)

# ---> find_most_similar
