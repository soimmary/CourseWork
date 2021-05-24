import csv
import os
import pickle
import numpy as np
import pandas as pd
from math import sqrt
from tqdm import tqdm


'''
# Вычисляем размер корпуса
corpora_path = '/Users/mariabocharova/PycharmProjects/Thesis/string_corpora.txt'
with open(corpora_path, 'r', encoding='utf-8') as f:
    corpora = f.read()


# Считаем частоту (ipm) вхождений слова на всем корпусе
def corpora_freq(term):
    global corpora, corpora_size
    term_freq = round(corpora.count(term) / 117000000 * 1000000, 2)
    return term_freq'''


# Считаем частоту (ipm) вхождений слова на всем корпусе
def freq(term):
    global corpora, corpora_size
    term_freq = round(corpora.count(term) / 117000000 * 1000000, 2)
    return term_freq


paths = ['/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/frequency_dict.csv',
         '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/bigram_frequency_dict.csv',
         '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/trigram_frequency_dict.csv',
         '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/fourgram_frequency_dict.csv',
         '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/fivegram_frequency_dict.csv']


'''for path in tqdm(paths):
    tqdm.pandas()
    df = pd.read_csv(path)
    df['частота (ipm)'] = df['термин'].progress_apply(freq)
    df.to_csv(f'{path[:-4]}_full.csv')'''


# Для вычисления коэффициента Жуайна разделим текст на ~ 1 000 одинаковых частей
def split_corpora(corpora_path):
    with open(corpora_path, 'r', encoding='utf-8') as f:
        i = 1
        slice = []
        for line in f:
            if len(slice) < 130000:
                slice.extend(line.split())
            else:
                with open(f'/Users/mariabocharova/PycharmProjects/Thesis/split_corpora/{i}_part.txt',
                          'w') as f1:
                    f1.write(' '.join(slice))
                    slice = []
                    i += 1
                    print('создан файл:', i)
        with open(f'/Users/mariabocharova/PycharmProjects/Thesis/split_corpora/{i}_part.txt',
                  'w') as f2:
            f2.write(' '.join(slice))


#split_corpora('/Users/mariabocharova/PycharmProjects/Thesis/corpora.txt')


# Считаем коэффициент Жуайна
def juilland_d(term, root_path):
    # n – количество сегментов, на которое развит корпус
    # μ – средняя частота слова по всему корпусу (mfrq)
    # σ – среднее квадратичное отклонение частоты μ на отдельных сегментах (rmse)
    segment_paths = [elem for elem in os.listdir(root_path) if not elem.startswith('.')]
    n = len(segment_paths)
    segment_freq = []
    for path in tqdm(segment_paths):
        with open(f'{root_path}/{path}') as f:
            segment_freq.append(f.read().count(term))
    rmse = np.std(segment_freq)
    mfrq = sum(segment_freq) / n
    jd = round(100 * (1 - (rmse / (mfrq * sqrt(n - 1)))), 3)
    r = (len(segment_freq)
    return jd, r


print(juilland_d('язык', '/Users/mariabocharova/PycharmProjects/Thesis/split_corpora'))


'''path = '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/frequency_dict_full.csv'
tqdm.pandas()
df = pd.read_csv(path)
df['R'] = df['термин'].progress_apply()
df['D'] = df['термин'].progress_apply()

juilland_d('/Users/mariabocharova/PycharmProjects/Thesis/split_corpora')
'''