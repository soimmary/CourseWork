import nltk
from nltk.collocations import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tqdm import tqdm
import pickle
import string
import csv
import os

stop_words = stopwords.words('russian')
stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'на', '?', 'который', 'мочь', 'наш', 'ваш', 'их', 'свой', 'иной'])
stop_words.extend(list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                       'ФБВГДЕЁДЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'))

all_bigrams = {}
all_trigrams = {}


def get_bigrams(path):
    global all_bigrams, stop_words
    with open(path, encoding='utf-8') as f:
        text = f.read()
        bigram_finder = BigramCollocationFinder.from_words(word_tokenize(text))
        top_bigram_raw = sorted(bigram_finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
        for bigram in top_bigram_raw:
            if bigram[0][0] not in stop_words and bigram[0][1] not in stop_words:
                if bigram[0] in all_bigrams:
                    all_bigrams[bigram[0]] += int(bigram[1])
                else:
                    all_bigrams[bigram[0]] = int(bigram[1])
                if bigram[1] <= int(len(text.split()) * 0.00005):
                    break
    with open('bigram_dict.pickle', 'wb') as f:
        pickle.dump(all_trigrams, f)
        print(path)


def get_trigrams(path):
    global all_trigrams, stop_words
    with open(path, encoding='utf-8') as f:
        text = f.read()
        trigram_finder = TrigramCollocationFinder.from_words(word_tokenize(text))
        top_trigram_raw = sorted(trigram_finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
        for trigram in top_trigram_raw:
            if trigram[0][0] not in stop_words and trigram[0][1] not in stop_words and trigram[0][2] not in stop_words:
                if trigram[0] in all_trigrams:
                    all_trigrams[trigram[0]] += int(trigram[1])
                else:
                    all_trigrams[trigram[0]] = int(trigram[1])
                if trigram[1] <= int(len(text.split()) * 0.00005):
                    break
    with open('trigram_dict.pickle', 'wb') as f:
        pickle.dump(all_trigrams, f)
        print(path)


common_path = '/Users/mariabocharova/PycharmProjects/Thesis/texts_by_year/texts_by_year_lemm'
paths = [f'{common_path}/{p}' for p in os.listdir(common_path)]
for path in tqdm(paths[1:3]):
    get_bigrams(path)
    # Записываем в csv файл биграммы
    with open('/Users/mariabocharova/PycharmProjects/Thesis/bigrams.csv', 'a') as csv_f:
        writer = csv.writer(csv_f, delimiter=',')
        for words, freq in all_bigrams.items():
            writer.writerow([words[0], words[1], freq])

    get_trigrams(path)
    # Записываем в csv файл триграммы
    with open('/Users/mariabocharova/PycharmProjects/Thesis/trigrams.csv', 'a') as csv_f:
        writer = csv.writer(csv_f, delimiter=',')
        for words, freq in all_trigrams.items():
            writer.writerow([words[0], words[1], words[2], freq])
