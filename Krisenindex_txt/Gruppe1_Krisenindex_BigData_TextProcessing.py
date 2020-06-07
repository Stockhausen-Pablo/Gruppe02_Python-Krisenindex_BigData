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
