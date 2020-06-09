#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:06:02 2020

@author: Paulo
"""

import os
import collections

dir_path = os.path.dirname(os.path.realpath(__file__))
Word_Bag = []
Anzahl_Bag = []
Bin_Bag = []
all_text_liste_k = []
all_text_liste_n = []
all_text_liste_c = []


def einlesen(x):
    if x == 'k':
        folder_path = dir_path + '/Krise'
    elif x == 'n':
        folder_path = dir_path + '/Normal'
    elif x == 'c':
        folder_path = dir_path + '/Corona'        
    subfolders_paths = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    for path in sorted(subfolders_paths):
        tag_liste_c = []
        files = os.listdir(path)
        for file in sorted(files):
            fullpath = path + '/' + file
            with open(fullpath, 'r', encoding="utf8") as file:
                if x == 'k':
                    all_text_liste_k.append(file.read())
                elif x == 'n':
                    all_text_liste_n.append(file.read())
                elif x == 'c':
                    tag_liste_c.append(file.read())
        if len(tag_liste_c) != 0:
            all_text_liste_c.append(" ".join(tag_liste_c).replace('.', ""))
    if x == 'k':
        return all_text_liste_k
    elif x == 'n':
        return all_text_liste_n 
    elif x == 'c':
        return all_text_liste_c 
 
# Vorkrisenzeit
all_text_string_k = " ".join(einlesen('k')).replace('.', "")
Tupel_Bag_k = collections.Counter(all_text_string_k.split())

# Normalzeit
all_text_string_n = " ".join(einlesen('n')).replace('.', "")
Tupel_Bag_n = collections.Counter(all_text_string_n.split())

del all_text_string_k, all_text_string_n

# Differenz
Tupel_Bag_k.subtract(Tupel_Bag_n)
Tupel_Bag = Tupel_Bag_k.most_common()

del Tupel_Bag_k, Tupel_Bag_n

# Sentiment
path_Senti_positive = dir_path + '/Senti/SentiWS_v2.0_Positive.txt'
#path_Senti_negative = dir_path + '/Senti/SentiWS_v2.0_Negative.txt'

Senti_positive = []
#Senti_negative = []

with open(path_Senti_positive, 'r', encoding="utf8") as file:
    Senti_positive = file.read().splitlines()

# with open(path_Senti_negative, 'r', encoding="utf8") as file:
#     Senti_negative = file.read().splitlines()
    
del path_Senti_positive

for index,element in enumerate(Senti_positive):
    m = element.index('|')    
    Senti_positive[index] = element[:m]

# for index,element in enumerate(Senti_negative):
#     m = element.index('|')    
#     Senti_negative[index] = element[:m]

del m, index

Tupel_Bag = Tupel_Bag[3:]

for tupel in Tupel_Bag:
    okay = True
    for word in Senti_positive:
        if word==tupel[0]:
            Tupel_Bag.remove(tupel)
            okay = False
            break
    if okay:    
        if tupel[1] >= 20:       
            Word_Bag.append(tupel[0])        
            Anzahl_Bag.append(tupel[1])
                
        else:           
            Bin_Bag.append(tupel[0])

## %%
# Corona

desc_l = []
tag_l = einlesen('c')

for tag in tag_l:
 
    l = tag.split()
    desc = [0] * len(Word_Bag) 
    for i, word in enumerate(Word_Bag):
        for x in l:
            if word == x:
                desc[i] += 1
    desc_l.append(desc)

## %%
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
#import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

desc_l.insert(0, Anzahl_Bag)
matrix = np.array(desc_l)  

similarities = cosine_similarity(sparse.csr_matrix(matrix))

y = list(similarities[:,0])
y = np.array(y[-len(tag_l):])
x = np.array(list(range(len(tag_l))))

d = {'x': x, 'y': y}
df = pd.DataFrame(d)
sns.set(style='darkgrid')
sns.lineplot(x='x', y='y', data=df)
