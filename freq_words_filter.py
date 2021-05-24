from tqdm import tqdm
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
import requests
import re
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER, LOC,
    NamesExtractor,
    Doc)


morph = MorphAnalyzer()
emb = NewsEmbedding()
segmenter = Segmenter()
morph_vocab = MorphVocab()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
names_extractor = NamesExtractor(morph_vocab)

stopwords = stopwords.words("russian")


def pos(x):
    p = morph.parse(x)[0]
    return p.tag.POS


def make_freq_dict(path):
    with open(path) as f:
        text = f.read()
        freq_terms = {}
        for word, freq in tqdm(Counter(text.split()).items()):
            if len(word) > 1 and word not in stopwords:
                freq_terms[word] = freq
        sorted_freq_words = sorted(freq_terms.items(), key=lambda a: a[1], reverse=True)
        print('number of terms after stop-words removal', len(sorted_freq_words))
    return sorted_freq_words


def make_db(sorted_freq_words):
    df = pd.DataFrame(sorted_freq_words)
    df = df.rename(columns={0: 'word', 1: 'freq'})
    df = df[df['freq'] >= 1000].dropna()
    df['pos'] = df['word'].apply(pos)
    print('number of terms after infrequent words removal:', len(df.values.tolist()))
    df = df[(df.pos == 'ADJF') | (df.pos == 'NOUN')]
    print('num of terms after leaving only NOUNs and ADJFs:', len(df.values.tolist()))
    return df.values.tolist()


# Фильтруем список терминов с помощью контрастного словаря
def filtering(all_ling_lemms):
    link_media = 'http://dict.ruslang.ru/freq.php?act=show&dic=freq_news&title=%D7%E0%F1%F2%EE%F2%ED%FB%E9%20%F1%EB%EE%E2%E0%F0%FC%20%EF%F3%E1%EB%E8%F6%E8%F1%F2%E8%EA%E8'
    link_fic = 'http://dict.ruslang.ru/freq.php?act=show&dic=freq_fiction&title=%D7%E0%F1%F2%EE%F2%ED%FB%E9%20%F1%EB%EE%E2%E0%F0%FC%20%F5%F3%E4%EE%E6%E5%F1%F2%E2%E5%ED%ED%EE%E9%20%EB%E8%F2%E5%F0%E0%F2%F3%F0%FB'
    media_set = set([i[4:-5] for i in re.findall(r'<td>[а-яёА-ЯЁ]+?</td>', requests.get(link_media).text)])
    nonfic_set = set([i[4:-5] for i in re.findall(r'<td>[а-яёА-ЯЁ]+?</td>', requests.get(link_fic).text)])

    # Фильтруем список лингвистических терминов
    ling_lemms = [(lemm[0], lemm[1]) for lemm in all_ling_lemms
                  if lemm[0] not in media_set or lemm[0] not in nonfic_set]
    print('number of terms after deleting common terms', len(ling_lemms))

    # Удаляем PER и LOC
    filtered_ling_lemms = []
    for lemm in ling_lemms:
        doc = Doc(lemm[0].title())
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)
        for span in doc.spans:
            span.normalize(morph_vocab)
        for span in doc.spans:
            if span.type == LOC or span.type == PER:
                span.extract_fact(names_extractor)
        if len(doc.spans) == 0:
            filtered_ling_lemms.append(lemm)
    print('number of terms after deleting PERs and LOCs', len(filtered_ling_lemms))
    db_ling = pd.DataFrame(filtered_ling_lemms)
    db_ling = db_ling.rename(columns={0: 'word', 1: 'freq'})
    db_ling.to_csv('/Users/mariabocharova/PycharmProjects/Thesis/freq_terms_filtered.csv')


filtering(make_db(make_freq_dict('/Users/mariabocharova/PycharmProjects/Thesis/string_corpora.txt')))
# --> find_most_similar
