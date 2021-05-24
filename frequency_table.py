import os
import csv
from tqdm import tqdm


"""
Создаем папку с текстами, сортированными по декаде
"""


def texts_by_decade(path_year, path_dec):
    by_year_paths = [i for i in os.listdir(path_year) if not i.startswith('.')]
    for path in by_year_paths:
        decade = path[:3]
        with open(f'{path_year}/{path}', 'r', encoding='utf-8') as f1:
            text = f1.read()
        with open(f'{path_dec}/{decade}0s.txt', 'a', encoding='utf-8') as f2:
            f2.write(text)


def corpora_size(path):
    corp_size = {}
    for dec in os.listdir(path):
        if not dec.startswith('.'):
            with open(f'{path}/{dec}', 'r', encoding='utf-8') as f:
                text_size = len(f.read().split())
                corp_size[dec[:-4]] = text_size
    return corp_size


def filling_table(terms, path_dec, aim_path):
    global corpora_size_dict
    with open(aim_path, 'a', encoding='utf-8') as csv_f:
        writer = csv.writer(csv_f, delimiter=',')
        writer.writerow(['лемма', 'частота (ipm)', '1960-е', '1970-е',
                         '1980-е', '1990-е', '2000-е', '2010-е', '2020-е'])
        for term in tqdm(terms):
            term_dict = {}
            for path in os.listdir(path_dec):
                if not path.startswith('.'):
                    with open(f'{path_dec}/{path}', 'r', encoding='utf-8') as f:
                        text = f.read()
                        term_dict[f'{path[:-5]}-е'] = str(round(text.count(term) * 1000000 / int(corpora_size_dict[f'{path[:-4]}']), 1))
            writer.writerow([term, None, term_dict['1960-е'], term_dict['1970-е'], term_dict['1980-е'],
                            term_dict['1990-е'], term_dict['2000-е'], term_dict['2010-е'], term_dict['2020-е']])


path_year = '/Users/mariabocharova/PycharmProjects/Thesis/texts_by_year/texts_by_year_lemm'
path_dec = '/Users/mariabocharova/PycharmProjects/Thesis/texts_by_decade'

corpora_size_dict = corpora_size('/Users/mariabocharova/PycharmProjects/Thesis/texts_by_decade')

with open('/Users/mariabocharova/PycharmProjects/Thesis/bigrams_filtered.csv', encoding='utf-8') as csvf_2:
    bigrams = [' '.join(ngram) for ngram in list(csv.reader(csvf_2))[977:]]
    filling_table(bigrams, path_dec, 'bigram_frequency_dict.csv')

with open('/Users/mariabocharova/PycharmProjects/Thesis/trigrams_filtered.csv', encoding='utf-8') as csvf_3:
    trigrams = [' '.join(ngram) for ngram in list(csv.reader(csvf_3))]
    filling_table(trigrams, path_dec, 'trigram_frequency_dict.csv')

with open('/Users/mariabocharova/PycharmProjects/Thesis/fourgrams_filtered.csv', encoding='utf-8') as csvf_4:
    fourgrams = [' '.join(ngram) for ngram in list(csv.reader(csvf_4))]
    filling_table(fourgrams, path_dec, 'fourgram_frequency_dict.csv')

with open('/Users/mariabocharova/PycharmProjects/Thesis/fivergrams_filtered.csv', encoding='utf-8') as csvf_5:
    fivegrams = [' '.join(ngram) for ngram in list(csv.reader(csvf_5))]
    filling_table(fivegrams, path_dec, 'fivegram_frequency_dict.csv')
