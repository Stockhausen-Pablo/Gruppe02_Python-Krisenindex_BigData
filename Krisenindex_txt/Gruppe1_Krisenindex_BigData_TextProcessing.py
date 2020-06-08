#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:06:02 2020
@author: Paulo
"""

#import spacy
import os
import collections

dir_path = os.path.dirname(os.path.realpath(__file__))
Word_Bag = []
Anzahl_Bag = []
Bin_Bag = []

# Vorkrisenzeit
path_kx = dir_path + '/Weltwirtschaftskrise/2008_08'
path_ky = dir_path + '/Weltwirtschaftskrise/2008_09'
all_text_liste_k = []
listOfFile_kx = os.listdir(path_kx)
listOfFile_ky = os.listdir(path_ky)

for file in listOfFile_kx:
    fullpath = path_kx + '/' + file
    with open(fullpath, 'r', encoding="utf8") as file:
        all_text_liste_k.append(file.read())
for file in listOfFile_ky:
    fullpath = path_ky + '/' + file
    with open(fullpath, 'r', encoding="utf8") as file:
        all_text_liste_k.append(file.read()) 

all_text_string_k = " ".join(all_text_liste_k).replace('.', "")

Tupel_Bag_k = collections.Counter(all_text_string_k.split())

# Normalzeit
path_nx = dir_path + '/Weltwirtschaftskrise_Normalzeit_text/2008_05'
path_ny = dir_path + '/Weltwirtschaftskrise_Normalzeit_text/2008_06'
all_text_liste_n = []
listOfFile_nx = os.listdir(path_nx)
listOfFile_ny = os.listdir(path_ny)

for file in listOfFile_nx:
    fullpath = path_nx + '/' + file
    with open(fullpath, 'r', encoding="utf8") as file:
        all_text_liste_n.append(file.read())
for file in listOfFile_ny:
    fullpath = path_ny + '/' + file
    with open(fullpath, 'r', encoding="utf8") as file:
        all_text_liste_n.append(file.read()) 

all_text_string_n = " ".join(all_text_liste_n).replace('.', "")

Tupel_Bag_n = collections.Counter(all_text_string_n.split())

# Differenz
Tupel_Bag_k.subtract(Tupel_Bag_n)
Tupel_Bag = Tupel_Bag_k.most_common()

for tupel in Tupel_Bag:
     
    if tupel[1] >= 5:       
        Word_Bag.append(tupel[0])        
        Anzahl_Bag.append(tupel[1])
            
    else:           
        Bin_Bag.append(tupel[0])
  del listOfFile_kx,listOfFile_ky,listOfFile_nx,listOfFile_ny,path_kx,path_ky,path_nx,path_ny, Tupel_Bag_k, Tupel_Bag_n,tupel 

# %%
#python -m nltk.downloader all
#<Word>|<POS tag> \t <Polarity weight> \t <Infl_1>,...,<Infl_k> \n
#https://wortschatz.uni-leipzig.de/de/download

# Path to both files
#path_Senti_negative = dir_path + '/Senti/SentiWS_v2.0_Negative.txt'
path_Senti_positive = dir_path + '/Senti/SentiWS_v2.0_Positive.txt'

Senti_positive = []
#Senti_negative = []

with open(path_Senti_positive, 'r', encoding="utf8") as file:
    Senti_positive = file.read().splitlines()

# with open(path_Senti_negative, 'r', encoding="utf8") as file:
#     Senti_negative = file.read().splitlines()
    
del path_Senti_positive

# Filter List after specific word

for index,element in enumerate(Senti_positive):
    m = element.index('|')    
    Senti_positive[index] = element[:m]

# for index,element in enumerate(Senti_negative):
#     m = element.index('|')    
#     Senti_negative[index] = element[:m]

# %%
del dir_path, m, index

#print(len(Word_Bag))

Word_Bag = list(filter(lambda x: x not in Senti_positive, Word_Bag))
           
#print(len(Word_Bag))
