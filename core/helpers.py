import fitz
import re
from pathlib import Path
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import pickle
import math
import os

MEDIA_DIR = os.path.join((Path(__file__).resolve().parent.parent), 'media/')
CORE_DIR = os.path.join((Path(__file__).resolve().parent.parent), 'core/')

print("---------------------------------")
print(MEDIA_DIR)
print(CORE_DIR)
print("---------------------------------")

def pdfToText(PDFName): #returns pathname
    doc = fitz.open(MEDIA_DIR + f'pdfUploads/{PDFName}')
    totalText = ""
    
    for page in doc:
        totalText += page.get_text("Text")
        
    outputFile = open(MEDIA_DIR + f'pdfToText/{PDFName[:-4]}.txt', 'w')
    outputFile.write(totalText)
    outputFile.close()
    
    return f'pdfToText/{PDFName[:-4]}.txt'


def generate_scrapes(query, num_urls=10):
    i=0
    url_file_map = {}
    urls = search(query, num=num_urls, pause=0.5, stop=num_urls)
    for url in urls:
        print(url)
        url_file_map[url] = f'scrapedText/scraped_dat_{i}.txt'
        response = requests.get(url)

        if response.status_code != 200:
            exit

        soup = BeautifulSoup(response.content, 'html5lib')
        data = soup.find_all('p')

        totalText = ""
        for extraction_p in data:
            extraction_p = re.sub('\[\d{0,}\]', '', extraction_p.text)
            extraction_p = re.sub('\[[a-z]\]', '', extraction_p)
            totalText += extraction_p
    
        with open(MEDIA_DIR + f'scrapedText/scraped_dat_{i}.txt', 'w') as f:
            f.write(totalText)
        i+=1
    
    print(url_file_map)
    return url_file_map

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk import ngrams
import pandas as pd
import numpy as np
import unicodedata

punctuation += "''``“”"

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

def predictPlag(param_array): # 2d array Input
    '''
    ONLY FOR PASSING PARAMETERS AND PREDICTING 0 or 1
    '''
    model_path = str(CORE_DIR)+'model_plag'
    with open(model_path, 'rb') as f:
        plag_model = pickle.load(f)
        prediction = plag_model.predict(param_array)[0]
        return prediction # 1 or 0

def features(test_text, scrape_text):
    word_freq_s, word_pair_s, trigram_s = word_frequency(scrape_text)
    string_token_s = stringTokenize(scrape_text)
    
    word_freq_t, word_pair_t, trigram_t = word_frequency(test_text)
    string_token_t = stringTokenize(test_text)
    
    
    word_freq_match = frequencyMatch(word_freq_s, word_freq_t)
    word_pair_match = frequencyMatch(word_pair_s, word_pair_t)
    trigram_match = frequencyMatch(trigram_s, trigram_t)
    sent_match = sentence_match(string_token_t, string_token_s).similarity.mean()
    if math.isnan(trigram_match):
        trigram_match = 0
    if math.isnan(word_pair_match):
        word_pair_match == 0
    if math.isnan(word_freq_match):
        word_freq_match = 0
    if math.isnan(sent_match):
        sent_match = 0
    
    paramArray = [[word_freq_match, word_pair_match, trigram_match, sent_match]]
    return paramArray

                                
def cleanWorkingTree():
    pdf2Text = MEDIA_DIR + '/pdfToText/'
    pdfUploads = MEDIA_DIR + '/pdfUploads/'
    scrapedText = MEDIA_DIR + '/scrapedText/'
    dir_list = [pdf2Text, pdfUploads, scrapedText]
    for directory in dir_list:
        dirs = os.listdir(directory)
        for file in dirs:
            os.remove(directory+file)


def prediction(testfilename, query, searchlevel):
    '''
    BINDER FUNCTION
    '''
    test_file_path = pdfToText(testfilename) # f'pdfToText/{PDFName[:-4]}.txt' TEST
    test_txt = openFile(MEDIA_DIR+test_file_path)
    url_file_map = generate_scrapes(query, searchlevel) # f'scrapedText/scraped_dat_{i}.txt' SCRAPES
    url_file_map = list(url_file_map)
    shady_urls = []
    for i in range(len(url_file_map)-1):
        scrape_file_path = f'scrapedText/scraped_dat_{i}.txt'
        scrape_txt = openFile(MEDIA_DIR+scrape_file_path)
        feats = features(test_txt, scrape_txt)
        result = predictPlag(feats)
        print(scrape_file_path)
        if result == 1:
            shady_urls.append(url_file_map[i])
    cleanWorkingTree()
    return result, shady_urls