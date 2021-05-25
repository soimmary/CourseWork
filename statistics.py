import csv
import os
import pickle
import numpy as np
import pandas as pd
from math import sqrt
from tqdm import tqdm


corpora_path = '/Users/mariabocharova/PycharmProjects/Thesis/string_corpora.txt'
with open(corpora_path, 'r', encoding='utf-8') as f:
    corpora = f.read()


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


for path in tqdm(paths):
    tqdm.pandas()
    df = pd.read_csv(path)
    df['частота (ipm)'] = df['термин'].progress_apply(freq)
    df.to_csv(f'{path[:-4]}_full.csv')


# Для вычисления коэффициента Жуайна разделим текст на ~ 1 000 одинаковых частей
def split_corpora(corpora_path):
    with open(corpora_path, 'r', encoding='utf-8') as f:
        i = 1
        slice = []
        for line in f:
            if len(slice) < 1200000:
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


# Считаем коэффициент Жуайна
def juilland_d(term):
    root_path = '/Users/mariabocharova/PycharmProjects/Thesis/split_corpora'
    # n – количество сегментов, на которое развит корпус
    # μ – средняя частота слова по всему корпусу (mfrq)
    # σ – среднее квадратичное отклонение частоты μ на отдельных сегментах (rmse)
    segment_paths = [elem for elem in os.listdir(root_path) if not elem.startswith('.')]
    n = len(segment_paths)
    freq = []
    freq_num = []
    for path in segment_paths:
        with open(f'{root_path}/{path}') as f:
            num = f.read().count(term)
            freq.append(num)
            if num > 0:
                freq_num.append(num)
    rmse = np.std(freq)
    mfrq = sum(freq) / n
    jd = round(100 * (1 - (rmse / (mfrq * sqrt(n - 1)))), 2)
    r = len(freq_num)
    return pd.Series([jd, r])


s = []
root_path = '/Users/mariabocharova/PycharmProjects/Thesis/split_corpora'
segment_paths = [elem for elem in os.listdir(root_path) if not elem.startswith('.')]
for path in tqdm(segment_paths):
    with open(f'{root_path}/{path}') as f:
        s.append(len(f.read().split()))
sum_s = sum(s)
for i in range(len(s)):
    s[i] = round(s[i] / sum_s, 3)
with open('s.pickle', 'wb') as f:
    pickle.dump(s, f)


# Deviation of Proportions
def dp(term):
    global s, segment_paths
    """
    n = 5: the length of the corpus in parts
    v = (1, 2, 3, 4, 5): the frequencies of a word in each corpus part 1-n
    f = 15: (he overall frequency of a word in the corpus
    s = (0.18, 0.2, 0.2, 0.2, 0.22): the percentages of the n corpus part sizes
    """
    n = len(segment_paths)
    v = []
    for path in segment_paths:
        with open(f'{root_path}/{path}') as f:
            text = f.read()
            num = text.count(term)
            v.append(num)
    sum_v = sum(v)
    for i in range(len(v)):
        v[i] = round(v[i] / sum_v, 3)
    f = sum(v)
    dp = 0
    for i in range(n):
        dp += 0.5 * (abs((v[i] / f) - s[i]))
    return round(dp, 4)


with open('s.pickle', 'rb') as f:
    s = pickle.load(f)

root_path = '/Users/mariabocharova/PycharmProjects/Thesis/split_corpora'
segment_paths = [elem for elem in os.listdir(root_path) if not elem.startswith('.')]

paths = ['/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/frequency_dict.csv',
         '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/bigram_frequency_dict.csv',
         '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/trigram_frequency_dict.csv',
         '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/fourgram_frequency_dict.csv',
         '/Users/mariabocharova/PycharmProjects/Thesis/lemmatization/fivegram_frequency_dict.csv']

for path in paths:
    df = pd.read_csv(path)
    tqdm.pandas()
    df[['DP']] = df['термин'].progress_apply(dp)
    tqdm.pandas()
    df[['D', 'R']] = df['термин'].progress_apply(juilland_d)
    df.to_csv(f'{path[:-4]}_2.csv')
