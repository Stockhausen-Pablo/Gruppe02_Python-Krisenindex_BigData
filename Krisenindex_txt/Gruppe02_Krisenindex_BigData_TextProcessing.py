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
ttf_vorkrisenzeit['positiv'] = [0]*len(ttf_vorkrisenzeit['Wort'])
ttf_vorkrisenzeit['negativ'] = [0]*len(ttf_vorkrisenzeit['Wort'])

ttf_normalzeit['Gewichtung'] = ttf_normalzeit['Anzahl']/sum(ttf_normalzeit['Anzahl'])
ttf_normalzeit['positiv'] = [0]*len(ttf_normalzeit['Wort'])
ttf_normalzeit['negativ'] = [0]*len(ttf_normalzeit['Wort'])

# Corona einlesen
# tag_l = einlesen('c')   

del index, count, tupel, Tupel_Bag_k, Tupel_Bag_n

#%%
# SENTI

path_Senti_negative = dir_path + '/Senti/SentiWS_v2.0_Negative.txt'
path_Senti_positive = dir_path + '/Senti/SentiWS_v2.0_Positive.txt'

Senti_positive = []
Senti_negative = []

with open(path_Senti_positive, 'r', encoding="utf8") as file:
    Senti_positive = file.read().splitlines()

with open(path_Senti_negative, 'r', encoding="utf8") as file:
    Senti_negative = file.read().splitlines()
    
# Filter List nach einem spezifischen Wort bis zum Symbol "|"
for index,element in enumerate(Senti_positive):
    m = element.index('|')    
    Senti_positive[index] = element[:m]

for index,element in enumerate(Senti_negative):
    m = element.index('|')    
    Senti_negative[index] = element[:m]

del path_Senti_negative,path_Senti_positive, index, m, element, file

for wort in Senti_negative:
    for i, term in enumerate(ttf_vorkrisenzeit['Wort']):
        if wort == term:
            ttf_vorkrisenzeit["negativ"][i] += 1
            break
        
    for i, term in enumerate(ttf_normalzeit['Wort']):
        if wort == term:
            ttf_normalzeit["negativ"][i] += 1
            break
        
for wort in Senti_positive:
    for i, term in enumerate(ttf_vorkrisenzeit['Wort']):
        if wort == term:
            ttf_vorkrisenzeit["positiv"][i] += 1
            break
        
    for i, term in enumerate(ttf_normalzeit['Wort']):
        if wort == term:
            ttf_normalzeit["positiv"][i] += 1
            break
        
del wort, i, term

#%%
# GEWICHTUNG MIT SENTI

Gewichtung_Senti = []

for i in range(len(ttf_vorkrisenzeit['Gewichtung'])):
    if ttf_vorkrisenzeit['negativ'][i] == 1:
        Gewichtung_Senti.append(ttf_vorkrisenzeit['Gewichtung'][i] * 4)
    elif ttf_vorkrisenzeit['positiv'][i] == 1:
        Gewichtung_Senti.append(ttf_vorkrisenzeit['Gewichtung'][i] * 0.25)
    else:
        Gewichtung_Senti.append(ttf_vorkrisenzeit['Gewichtung'][i])

ttf_vorkrisenzeit['Gewichtung Senti'] = Gewichtung_Senti/sum(Gewichtung_Senti)

Gewichtung_Senti = []

for i in range(len(ttf_normalzeit['Gewichtung'])):
    if ttf_normalzeit['positiv'][i] == 1:
        Gewichtung_Senti.append(ttf_normalzeit['Gewichtung'][i] * 4)
    elif ttf_normalzeit['negativ'][i] == 1:
        Gewichtung_Senti.append(ttf_normalzeit['Gewichtung'][i] * 0.25)
    else:
        Gewichtung_Senti.append(ttf_normalzeit['Gewichtung'][i])

ttf_normalzeit['Gewichtung Senti'] = Gewichtung_Senti/sum(Gewichtung_Senti)

del i, Gewichtung_Senti

#%%
# DESKRIPTOREN ERSTELLEN/EINLESEN

import numpy as np

# EINLESEN
deskriptoren_vorkrise = np.loadtxt('Matrix_Vorkrise_Politik_NEW.txt', dtype=float)
deskriptoren_normal = np.loadtxt('Matrix_Normal_Politik_NEW.txt', dtype=float)

# ERSTELLEN
# deskriptoren_vorkrise_1 = np.zeros((len(tag_l), len(ttf_vorkrisenzeit)))
# deskriptoren_normal_1 = np.zeros((len(tag_l), len(ttf_normalzeit)))

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
    score = sum(deskriptoren_vorkrise[i] * np.array(ttf_vorkrisenzeit['Gewichtung Senti']))
    score_vorkrise.append(score)

for i in range(len(deskriptoren_normal)):
    score = sum(deskriptoren_normal[i] * np.array(ttf_normalzeit['Gewichtung Senti']))
    score_normal.append(score)      

del i, score

score_df = pd.DataFrame({'Vorkrise': score_vorkrise, 'Normal': score_normal})     
score_df['p(Vorkrise)'] = score_df['Vorkrise']/(score_df['Vorkrise']+score_df['Normal'])
score_df['p(Normal)'] = score_df['Normal']/(score_df['Vorkrise']+score_df['Normal'])
score_df['Differenz'] = score_df['p(Vorkrise)']-score_df['p(Normal)']
score_df['Kommt Krise?'] = np.where((score_df['p(Vorkrise)'] > score_df['p(Normal)']), 1, 0)


score_df['date'] = pd.date_range(start='1/1/2019', periods=len(score_df), freq='D')
del score_normal, score_vorkrise

#%%
# DARSTELLUNG

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('dark')
sns.set(font_scale=2.3)
fig, ax1 = plt.subplots(figsize=(25, 12))
sns.lineplot(x='date', y='p(Normal)', data=score_df, ax=ax1, label="Normal")
sns.lineplot(x='date', y='p(Vorkrise)', data=score_df, ax=ax1, label="Vorkrise")
ax1.legend()
sns.despine(fig)

fig, ax1 = plt.subplots(figsize=(25, 12))
sns.lineplot(x='date', y='p(Normal)', data=score_df[300:], ax=ax1, label="Normal")
sns.lineplot(x='date', y='p(Vorkrise)', data=score_df[300:], ax=ax1, label="Vorkrise")
ax1.legend()
sns.despine(fig)

fig, ax1 = plt.subplots(figsize=(25, 12))
sns.lineplot(x='date', y='Differenz', data=score_df, ax=ax1, label="Differenz")
sns.lineplot(x='date', y=0, data=score_df, ax=ax1)
ax1.legend()
sns.despine(fig)

#%%
# MATRIZEN SPEICHERN

# np.savetxt('Matrix_Vorkrise_Politik_NEW.txt', deskriptoren_vorkrise, fmt='%d')
# np.savetxt('Matrix_Normal_Politik_NEW.txt', deskriptoren_normal, fmt='%d')
