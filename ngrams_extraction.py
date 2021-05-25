from nltk.util import ngrams
from nltk.corpus import stopwords
from tqdm import tqdm
from collections import Counter
import pickle
import csv
import os


stop_words = stopwords.words('russian')
stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'на', '?',
                   'который', 'мочь', 'наш', 'ваш', 'их', 'свой', 'иной'])
stop_words.extend(list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                       'ФБВГДЕЁДЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'))

all_bigrams = {}
all_trigrams = {}
all_fourgrams = {}
all_fivegrams = {}

with open('/Users/mariabocharova/PycharmProjects/Thesis/all_terms_4.2.csv',
          'r', encoding='utf-8') as csvf:
    ling_terms = set([term[0] for term in csv.reader(csvf)])


def get_bigrams(path):
    global stop_words, all_bigrams, ling_terms
    with open(path, encoding='utf-8') as f:
        text = f.read().split()
        bigram_finder = ngrams(text, 2)
        bigrams_unfiltered = Counter(list(bigram_finder))
        for bigram in bigrams_unfiltered.items():
            # проверка на стоп-слова
            if bigram[0][0] not in stop_words and bigram[0][1] not in stop_words:
                # проверка, есть ли лексемы из n-грамма в словаре линг. терминов
                if bigram[0][0] in ling_terms or bigram[0][1] in ling_terms:
                    if bigram[0] in all_bigrams:
                        all_bigrams[bigram[0]] += bigram[1]
                    else:
                        all_bigrams[bigram[0]] = bigram[1]
    with open('bigram_dict.pickle', 'wb') as f:
        pickle.dump(all_bigrams, f)


def get_trigrams(path):
    global stop_words, all_trigrams, ling_terms
    with open(path, encoding='utf-8') as f:
        text = f.read().split()
        trigram_finder = ngrams(text, 3)
        trigrams_unfiltered = Counter(list(trigram_finder))
        for trigram in trigrams_unfiltered.items():
            # проверка на стоп-слова
            if trigram[0][0] not in stop_words and trigram[0][1] not in stop_words and \
                    trigram[0][2] not in stop_words:
                # проверка, есть ли лексемы из n-грамма в словаре линг. терминов
                if trigram[0][0] in ling_terms or trigram[0][1] in ling_terms or \
                        trigram[0][2] in ling_terms:
                    if trigram[0] in all_trigrams:
                        all_trigrams[trigram[0]] += trigram[1]
                    else:
                        all_trigrams[trigram[0]] = trigram[1]
    with open('trigram_dict.pickle', 'wb') as f:
        pickle.dump(all_trigrams, f)


def get_fourgrams(path):
    global stop_words, all_fourgrams, ling_terms
    with open(path, encoding='utf-8') as f:
        text = f.read().split()
        fourgram_finder = ngrams(text, 4)
        fourgrams_unfiltered = Counter(list(fourgram_finder))
        for fourgram in fourgrams_unfiltered.items():
            # проверка на стоп-слова
            if fourgram[0][0] not in stop_words and fourgram[0][1] not in stop_words and \
                    fourgram[0][2] not in stop_words and fourgram[0][3] not in stop_words:
                # проверка, есть ли лексемы из n-грамма в словаре линг. терминов
                if fourgram[0][0] in ling_terms or fourgram[0][1] in ling_terms or \
                        fourgram[0][2] in ling_terms or fourgram[0][3] in ling_terms:
                    if fourgram[0] in all_fourgrams:
                        all_fourgrams[fourgram[0]] += fourgram[1]
                    else:
                        all_fourgrams[fourgram[0]] = fourgram[1]
    with open('fourgram_dict.pickle', 'wb') as f:
        pickle.dump(all_fourgrams, f)


def get_fivegrams(path):
    global stop_words, all_fivegrams, ling_terms
    with open(path, encoding='utf-8') as f:
        text = f.read().split()
        fivegram_finder = ngrams(text, 5)
        fivegrams_unfiltered = Counter(list(fivegram_finder))
        for fivegram in fivegrams_unfiltered.items():
            # проверка на стоп-слова
            if fivegram[0][0] not in stop_words and fivegram[0][1] not in stop_words and \
                    fivegram[0][2] not in stop_words and fivegram[0][3] not in stop_words and \
                    fivegram[0][4] not in stop_words:
                # проверка, есть ли лексемы из n-грамма в словаре линг. терминов
                if fivegram[0][0] in ling_terms or fivegram[0][1] in ling_terms or \
                        fivegram[0][2] in ling_terms or fivegram[0][3] in ling_terms or \
                        fivegram[0][4] in ling_terms:
                    if fivegram[0] in all_fivegrams:
                        all_fivegrams[fivegram[0]] += fivegram[1]
                    else:
                        all_fivegrams[fivegram[0]] = fivegram[1]
    with open('fivegram_dict.pickle', 'wb') as f:
        pickle.dump(all_fivegrams, f)


def make_csv(common_path):
    global all_bigrams, all_trigrams, all_fourgrams, all_fivegrams
    paths = [f'{common_path}/{p}' for p in os.listdir(common_path) if not p.startswith('.')]
    for path in tqdm(paths):
        """get_bigrams(path)
        # Записываем в csv файл биграммы
    with open('/Users/mariabocharova/PycharmProjects/Thesis/bigrams.csv', 'a', encoding='utf-8') as csv_bi:
        writer = csv.writer(csv_bi, delimiter=',')
        all_bigrams = sorted(all_bigrams.items(), key=lambda item: item[1], reverse=True)
        for words, freq in all_bigrams:
            if freq > 1000:
                writer.writerow([words[0], words[1], freq])


        get_trigrams(path)
        # Записываем в csv файл триграммы
    with open('/Users/mariabocharova/PycharmProjects/Thesis/trigrams.csv', 'a') as csv_tri:
        writer = csv.writer(csv_tri, delimiter=',')
        all_trigrams = sorted(all_trigrams.items(), key=lambda item: item[1], reverse=True)
        for words, freq in all_trigrams:
            if freq >= 500:
                writer.writerow([words[0], words[1], words[2], freq])"""

        get_fourgrams(path)
        # Записываем в csv файл триграммы
    with open('/Users/mariabocharova/PycharmProjects/Thesis/fourgrams_2.csv', 'a') as csv_four:
        writer = csv.writer(csv_four, delimiter=',')
        all_fourgrams = sorted(all_fourgrams.items(), key=lambda item: item[1], reverse=True)
        for words, freq in all_fourgrams:
            writer.writerow([words[0], words[1], words[2], words[3], freq])

        get_fivegrams(path)
        # Записываем в csv файл триграммы
    with open('/Users/mariabocharova/PycharmProjects/Thesis/fivegrams.csv', 'a') as csv_five:
        writer = csv.writer(csv_five, delimiter=',')
        all_fivegrams = sorted(all_fivegrams.items(), key=lambda item: item[1], reverse=True)
        for words, freq in all_fivegrams:
            writer.writerow([words[0], words[1], words[2], words[3], words[4], freq])


make_csv('/Users/mariabocharova/PycharmProjects/Thesis/texts_by_year/texts_by_year_lemm')


