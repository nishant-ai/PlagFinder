from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk import ngrams
import pandas as pd
import numpy as np
import unicodedata
import re

punctuation += "’"

def openFile(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

def word_frequency(text):
    paragraph = text

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(paragraph)
    filtered_tokens = [word for word in word_tokens if (not word.lower() in stop_words) and (not word.lower() in punctuation)]

    lemmatizer = WordNetLemmatizer()
    filtered_tokens =[lemmatizer.lemmatize(t) for t in filtered_tokens]

    counted = Counter(filtered_tokens)
    counted_2= Counter(ngrams(filtered_tokens,2))
    counted_3= Counter(ngrams(filtered_tokens,3))

    word_freq = pd.DataFrame(counted.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)
    word_pairs = pd.DataFrame(counted_2.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)
    trigrams = pd.DataFrame(counted_3.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)

    return word_freq, word_pairs, trigrams

def frequencyMatch(df_scraped , df_test):
    merged = df_scraped.set_index("word").join(df_test.set_index("word"), lsuffix='_scraped', rsuffix='_test')
    merged = merged.fillna(0)
    frequency_match = merged.frequency_test*100 / merged.frequency_scraped
    merged['frequency_match'] = frequency_match
    merged.frequency_match = np.where(merged.frequency_match < 0, 0, merged.frequency_match)
    return merged.describe()

# ________________________________________

def stringTokenize(text):
    text = unicodedata.normalize("NFKD", text)
    stringTokens = sent_tokenize(text)
    return stringTokens

def sentence_match(testTokenSet, scrapeTokenSet):
    matchMap = []
    for test_token in testTokenSet:
        word_freq_test, pair_freq_test, trigram_freq_test = word_frequency(test_token)
        for scrape_token in scrapeTokenSet:
            word_freq_scrape, pair_freq_scrape, trigram_freq_scrape = word_frequency(scrape_token)
            match_table = frequencyMatch(word_freq_test, word_freq_scrape)
            match_mean = match_table.frequency_match[1] # mean
            if match_mean == 0:
                continue
            matchMap.append({
                'test_token' : test_token,
                'scrape_token' : scrape_token,
                'similarity' : match_mean
            })
    matchMap = pd.DataFrame(matchMap)
    return matchMap

