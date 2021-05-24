import re
import csv
from tqdm import tqdm
from gensim.models import Word2Vec


model = Word2Vec.load('ling_corpora_word2vec.model')


def get_terms(path):
    global all_terms
    with open(path, 'r', encoding='utf-8') as csvfile:
        terms = set()
        words = list(csv.reader(csvfile, delimiter=','))
        for word in words[1:]:
            terms.add(word[0])
    all_terms = all_terms | terms
    return all_terms


def get_extra_terms(n1, n2):
    global all_terms, model
    terms_1st_layer = set()
    terms_2nd_layer = set()
    for term1 in tqdm(list(all_terms)):
        try:
            for i in model.wv.most_similar(term1, topn=n1):
                if not re.search(r'[А-ЯЁA-Z]', i[0]):
                    terms_1st_layer.add(i[0])
        except KeyError:
            continue
    print(terms_1st_layer)

    for term2 in tqdm(list(terms_1st_layer)):
        try:
            for i in model.wv.most_similar(term2, topn=n2):
                if not re.search(r'[А-ЯЁA-Z]', i[0]):
                    terms_2nd_layer.add(i[0])
        except KeyError:
            continue
    print(terms_2nd_layer)

    all_terms |= terms_1st_layer
    all_terms |= terms_2nd_layer


get_terms('/Users/mariabocharova/PycharmProjects/Thesis/freq_terms_filtered.csv')
get_extra_terms(4, 2)

with open('/Users/mariabocharova/PycharmProjects/Thesis/all_terms_4.2.csv',
          'a', encoding='utf-8') as csvf:
    writer = csv.writer(csvf)
    for term in sorted(list(all_terms)):
        writer.writerow([term])

