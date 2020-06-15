#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:06:02 2020

@author: Gruppe 02
"""

# DATEN EINLESEN

import os
from collections import Counter
from itertools import chain
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))

def einlesen(x):
    all_text_liste = []
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
            with open(fullpath, 'r', encoding="utf-8") as file:
                if x == 'c':
                    try:
                        tag_liste_c.append(file.read())
                    except: pass    
                else:
                    all_text_liste.append(file.read())
        if len(tag_liste_c) != 0:
            all_text_liste.append(" ".join(tag_liste_c).replace('.', ""))
    return all_text_liste 
 
# Vorkrisenzeit einlesen

Tupel_Bag_k = Counter(chain.from_iterable(map(str.split, einlesen('k')))).most_common()

count = 0
for index, tupel in enumerate(Tupel_Bag_k):
    if tupel[1]>5000:
        count += 1
    elif tupel[1]==29:
        Tupel_Bag_k = Tupel_Bag_k[count:index]
        break

# Normalzeit einlesen

Tupel_Bag_n = Counter(chain.from_iterable(map(str.split, einlesen('n')))).most_common()

count = 0
for index, tupel in enumerate(Tupel_Bag_n):
    if tupel[1]>5000:
        count += 1
    elif tupel[1]==29:
        Tupel_Bag_n = Tupel_Bag_n[count:index]
        break

# auf gleiche Länge bringen

Tupel_Bag_n = Tupel_Bag_n[:len(Tupel_Bag_k)] 

# TTF zu Panda
ttf_vorkrisenzeit = pd.DataFrame(list(Tupel_Bag_k), columns=['Wort', 'Anzahl'])
ttf_normalzeit = pd.DataFrame(list(Tupel_Bag_n), columns=['Wort', 'Anzahl'])

# Gewichtung hinzufügen
ttf_vorkrisenzeit['Gewichtung'] = ttf_vorkrisenzeit['Anzahl']/sum(ttf_vorkrisenzeit['Anzahl'])
ttf_normalzeit['Gewichtung'] = ttf_normalzeit['Anzahl']/sum(ttf_normalzeit['Anzahl'])

# Corona einlesen
tag_l = einlesen('c')   

del index, count, tupel, Tupel_Bag_k, Tupel_Bag_n


#%%
# DESKRIPTOREN ERSTELLEN/EINLESEN

import numpy as np

# EINLESEN
deskriptoren_vorkrise = np.loadtxt('Matrix_Vorkrise_Politik_NEW.txt', dtype=float)
deskriptoren_normal = np.loadtxt('Matrix_Normal_Politik_NEW.txt', dtype=float)

# ERSTELLEN
# deskriptoren_vorkrise = np.zeros((len(tag_l), len(ttf_vorkrisenzeit)))
# deskriptoren_normal = np.zeros((len(tag_l), len(ttf_normalzeit)))

# for i, tag in enumerate(tag_l):
#     for wort in tag.split():
#         for j, term in enumerate(ttf_vorkrisenzeit['Wort']):
#             if wort == term:
#                 deskriptoren_vorkrise[i][j] += 1
#                 break
#     print("Vorkrise: Deskriptor " + str(i + 1) + " von " + str(len(tag_l)))
    
# for i, tag in enumerate(tag_l):
#     for wort in tag.split():
#         for j, term in enumerate(ttf_normalzeit['Wort']):
#             if wort == term:
#                 deskriptoren_normal[i][j] += 1
#                 break
#     print("Normal: Deskriptor " + str(i + 1) + " von " + str(len(tag_l)))
    
# del wort, term, i, j, tag
     
#%%
# SCORE BERECHNEN

score_vorkrise = []
score_normal = []

for i in range(len(deskriptoren_vorkrise)):
    score = sum(deskriptoren_vorkrise[i] * np.array(ttf_vorkrisenzeit['Gewichtung']))
    score_vorkrise.append(score)

for i in range(len(deskriptoren_normal)):
    score = sum(deskriptoren_normal[i] * np.array(ttf_normalzeit['Gewichtung']))
    score_normal.append(score)      

del i, score

score_df = pd.DataFrame({'Vorkrise': score_vorkrise, 'Normal': score_normal})     
score_df['p(Vorkrise)'] = score_df['Vorkrise']/(score_df['Vorkrise']+score_df['Normal'])
score_df['p(Normal)'] = score_df['Normal']/(score_df['Vorkrise']+score_df['Normal'])

score_df['Kommt Krise?'] = np.where((score_df['p(Vorkrise)'] > score_df['p(Normal)']), 1, 0)

del score_normal, score_vorkrise

#%%
# DARSTELLUNG

import matplotlib.pyplot as plt

score_df.plot(kind='line',y='p(Vorkrise)', color='red', ax=plt.gca())
score_df.plot(kind='line',y='p(Normal)', ax=plt.gca())

plt.show()

score_df[300:].plot(kind='line',y='p(Vorkrise)', color='red', ax=plt.gca())
score_df[300:].plot(kind='line',y='p(Normal)', ax=plt.gca())

plt.show()
#%%
# MATRIZEN SPEICHERN

np.savetxt('Matrix_Vorkrise_Politik_NEW.txt', deskriptoren_vorkrise, fmt='%d')
np.savetxt('Matrix_Normal_Politik_NEW.txt', deskriptoren_normal, fmt='%d')
