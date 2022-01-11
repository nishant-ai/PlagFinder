import pandas as pd
import numpy as np

corpus = pd.read_csv('data_set.csv')

for file in corpus.file:
    file = open('corpus/'+file, 'r', errors='ignore')
    print(file.read())
    
    