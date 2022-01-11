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
import os
import pickle

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
    frequency_match = merged.frequency_test*100/merged.frequency_scraped
    merged['frequency_match'] = frequency_match
    merged.frequency_match = np.where(merged.frequency_match < 0, 0, merged.frequency_match)
    merged.frequency_match = np.where(merged.frequency_match > 100, 100, merged.frequency_match)
    merged = merged.drop(merged[merged.frequency_test == 0].index)
#     print(merged)
    return merged['frequency_match'].mean()

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
            match_mean = frequencyMatch(word_freq_test, word_freq_scrape)
            matchMap.append({
                'test_token' : test_token,
                'scrape_token' : scrape_token,
                'similarity' : match_mean
                })
    matchMap = pd.DataFrame(matchMap)
    matchMap = matchMap[matchMap['similarity'].notna()]
    return matchMap

def initFeatureExtractions(n=160):
    file = open('features.csv', 'a')
    for i in range(n):
        try:
            scrape_text = openFile(f'scraped/scraped_test_{i}.txt')
            test_file_0 = f'test/test_file_{i}_0.txt'
            test_file_1 = f'test/test_file_{i}_1.txt'
            
            word_freq_s, word_pair_s, trigram_s = word_frequency(scrape_text)
            string_token_s = stringTokenize(scrape_text)
            
            if os.path.isfile(test_file_0):
                test_file_0 = openFile(f'test/test_file_{i}_0.txt')
                word_freq_t, word_pair_t, trigram_t = word_frequency(test_file_0)
                string_token_t = stringTokenize(test_file_0)
                plag = 0
            else:
                test_file_1 = openFile(f'test/test_file_{i}_1.txt')
                word_freq_t, word_pair_t, trigram_t = word_frequency(test_file_1)
                string_token_t = stringTokenize(test_file_1)
                plag = 1
            
            word_freq_match = frequencyMatch(word_freq_s, word_freq_t).frequency_match
            word_pair_match = frequencyMatch(word_pair_s, word_pair_t).frequency_match
            trigram_match = frequencyMatch(trigram_s, trigram_t).frequency_match
            word_mean, word_std, word_max = word_freq_match[1], word_freq_match[2], word_freq_match[7]
            pair_mean, pair_std, pair_max = word_pair_match[1], word_pair_match[2], word_pair_match[7]
            trigram_mean, trigram_std, trigram_max = trigram_match[1], trigram_match[2], trigram_match[7]
            sent_match = sentence_match(string_token_t, string_token_s).similarity.mean()
            
            print(f'{word_mean}, {word_std}, {word_max}, {pair_mean}, {pair_std}, {pair_max}, {trigram_mean}, {trigram_std}, {trigram_max}, {sent_match}, {plag}\n')
                
            file.write((f'{word_mean}, {word_std}, {word_max}, {pair_mean}, {pair_std}, {pair_max}, {trigram_mean}, {trigram_std}, {trigram_max}, {sent_match}, {plag}\n'))
    
        except Exception:
            print(Exception)
    
    file.close()
    
initFeatureExtractions()

def predictPlag(param_array): # 2d array Input
    with open('model_plag', 'rb') as f:
        plag_model = pickle.load(f)
        prediction = plag_model.predict(param_array)[0]
        return prediction # 1 or 0