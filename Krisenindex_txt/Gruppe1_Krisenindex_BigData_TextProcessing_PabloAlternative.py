#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:06:02 2020
@author: Gruppe 2
"""

"""
Stand: 10.06.2020, 
betrachet wird zunächst nur der Zeitraum aus der Weltwirtschaftskrise
"""

#import spacy
import os
import collections

current_dir_path = os.path.dirname(os.path.realpath(__file__))

# %%
"""
Texte der Vorkrisenzeit holen und in einer Liste abspeichern
"""

#Path zu den Ordner der Vorkrisenzeit
path_krisenzeit_aug = current_dir_path + '/Krise/Weltwirtschaftskrise/2008_08'
path_krisenzeit_sep = current_dir_path + '/Krise/Weltwirtschaftskrise/2008_09'

#Alle Filenames als Liste in den jeweiligen Ordnern
listOfFiles_krisenzeit_aug = os.listdir(path_krisenzeit_aug)
listOfFiles_krisenzeit_sep = os.listdir(path_krisenzeit_sep)

# Liste für Texte deklarieren
text_liste_vorkrise = []

#Auslesen und in die Liste abspeichern
for file in listOfFiles_krisenzeit_aug:
    fullpath = path_krisenzeit_aug + '/' + file
    with open(fullpath, 'r', encoding="utf8") as file:
        text_liste_vorkrise.append(file.read())

for file in listOfFiles_krisenzeit_sep:
    fullpath = path_krisenzeit_sep + '/' + file
    with open(fullpath, 'r', encoding="utf8") as file:
        text_liste_vorkrise.append(file.read())

del path_krisenzeit_aug, path_krisenzeit_sep, listOfFiles_krisenzeit_aug, listOfFiles_krisenzeit_sep

# %%
"""
Texte der Normalzeit holen und in einer Liste abspeichern
"""

#Path zu den Ordner der Normalzeit
path_normalzeit_mai  = current_dir_path + '/Normal/Weltwirtschaftskrise/2008_05'
path_normalzeit_juni = current_dir_path + '/Normal/Weltwirtschaftskrise/2008_06'

#Alle Filenames als Liste in den jeweiligen Ordnern
listOfFiles_normalzeit_mai = os.listdir(path_normalzeit_mai)
listOfFiles_normalzeit_juni = os.listdir(path_normalzeit_juni)

# Liste für Texte deklarieren
text_liste_normalzeit = []

#Auslesen und in die Liste abspeichern
for file in listOfFiles_normalzeit_mai:
    fullpath = path_normalzeit_mai + '/' + file
    with open(fullpath, 'r', encoding="utf8") as file:
        text_liste_normalzeit.append(file.read())

for file in listOfFiles_normalzeit_juni:
    fullpath = path_normalzeit_juni + '/' + file
    with open(fullpath, 'r', encoding="utf8") as file:
        text_liste_normalzeit.append(file.read())

del path_normalzeit_mai, path_normalzeit_juni, listOfFiles_normalzeit_mai, listOfFiles_normalzeit_juni
del fullpath, file

# %%
"""
Texte der Corona Zeit einlesen und speichern. (Benötigt als Awendungsfall)
"""

#Path zu den Ordner der Coronazeit
folder_path = current_dir_path + '/Corona'
subfolders_paths = [f.path for f in os.scandir(folder_path) if f.is_dir()]

#Liste für Texte deklarieren
text_liste_coronazeit = []

for path in sorted(subfolders_paths):
    #Alle Filenames als Liste in den jeweiligen Ordnern
    listOfFiles_coronazeit = os.listdir(path)
    for file in sorted(listOfFiles_coronazeit):
        fullpath = path + '/' + file
        with open(fullpath, 'r', encoding="utf8") as file:
             text_liste_coronazeit.append(file.read())
             
del path, listOfFiles_coronazeit, fullpath, folder_path, subfolders_paths

# %%
"""
Für Corona speziell alle Texte zu einer Wortliste transformieren
"""
wordlist_corona = []

for text in text_liste_coronazeit:
    wordlist_corona.append(text.split())

# %%
"""
Total Term Frequency in den jeweiligen Zeiten abspeichern
"""
from collections import Counter
from itertools import chain
import pandas as pd 

counter_vorkrisenzeit = Counter(chain.from_iterable(map(str.split, text_liste_vorkrise))) 
vorkrisenzeit_ttf = pd.Series(counter_vorkrisenzeit).sort_values(ascending=False)

counter_normalzeit = Counter(chain.from_iterable(map(str.split, text_liste_normalzeit))) 
normalzeit_ttf = pd.Series(counter_normalzeit).sort_values(ascending=False)

del counter_vorkrisenzeit, counter_normalzeit

# %%
"""
Wörter mit einer positiven Konnotation aus der Vorkrisenzeit entfernen
Zunächst müssen wir uns die Wörter holen und bearbeitbar machen
"""
#python -m nltk.downloader all
#<Word>|<POS tag> \t <Polarity weight> \t <Infl_1>,...,<Infl_k> \n
#https://wortschatz.uni-leipzig.de/de/download

#Pfad zu beiden text files
path_Senti_negative = current_dir_path + '/Senti/SentiWS_v2.0_Negative.txt'
path_Senti_positive = current_dir_path + '/Senti/SentiWS_v2.0_Positive.txt'

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

#Nun überprüfen wir, ob die Wörter in den jeweiligen 
#TTF-Listen vorkommen und löschen diese

vorkrisenzeit_ttf = vorkrisenzeit_ttf.loc[~vorkrisenzeit_ttf.index.isin(Senti_positive)]

normalzeit_ttf    = normalzeit_ttf.loc[~normalzeit_ttf.index.isin(Senti_negative)]

# %%
"""
Nicht-Aussagekräftige Anzahl von Wörtern entfernen
"""

vorkrisenzeit_ttf = vorkrisenzeit_ttf[vorkrisenzeit_ttf > 50][vorkrisenzeit_ttf < 10000]

normalzeit_ttf    = normalzeit_ttf[normalzeit_ttf > 50][normalzeit_ttf < 10000]

# %%
"""
Die TTF Series als Dataframe abspeichern, da wir nun damit weiter arbeiten
werden
"""
df_vorkrisenzeit = pd.DataFrame({'Terms':vorkrisenzeit_ttf.index, 'Anzahl':vorkrisenzeit_ttf.values,"Art":"Vorkrisenzeit","ArtNr":1})

df_normalzeit    = pd.DataFrame({'Terms':normalzeit_ttf.index, 'Anzahl':normalzeit_ttf.values,"Art":"Normalzeit","ArtNr":2})

# %%
"""
Deskriptoren aufbereiten
"""
import numpy as np

deskriptor_normalzeit     = np.zeros((1,len(df_normalzeit)))

deskriptor_vorkrisenzeit  = np.zeros((1,len(df_vorkrisenzeit)))

deskriptor_Senti_positive = np.zeros((1,len(Senti_positive)))

deskriptor_Senti_negative = np.zeros((1,len(Senti_negative)))

# %%
"""
Wir stellen nun die Diskreptoren auf für die eingelesenen
Anwedungsfall-Texte. Wir betrachten die Vorkrisenzeit, Normalzeit, sowie 
die negativ und postive Wörterlisten der Sentiment Analyse.
"""

#Wir benutzen die Umwandlung in ein set für den schnelleren
#Suchalgorithmus --> Liste ist sehr groß
set_vorkrise_terms = set(df_vorkrisenzeit.Terms) 
set_normal_terms   = set(df_normalzeit.Terms)
set_positive_terms = set(Senti_positive)
set_negative_terms = set(Senti_negative)

#Liste mit den indexen, die wir später in den jeweiligen 
#Deskriptoren um 1 erhöhen müssen
index_gefunden_vorkrise   = []
index_gefunden_normal     = []
index_gefunden_positive   = []
index_gefunden_negative   = []

#Doppelte Schleife für jede Liste(Einzelnen Artikeln) innerhalb der Artikeliste 
#dann die einzelnen Worlisten der Artikel.
#Anschließend abgleich, ob der Term in den sets vorkommt.
for liste in wordlist_corona:
    for term_corona in liste:
        if term_corona in set_normal_terms:
            index_normal, = df_normalzeit.loc[df_normalzeit.Terms == term_corona].index
            index_gefunden_normal.append(index_normal)
        if term_corona in set_vorkrise_terms:
            index_vorkrise, = df_vorkrisenzeit.loc[df_vorkrisenzeit.Terms == term_corona].index
            index_gefunden_vorkrise.append(index_vorkrise)
        if term_corona in set_positive_terms:
            index_positive = Senti_positive.index(term_corona)
            index_gefunden_positive.append(index_positive)
        if term_corona in set_negative_terms:
            index_negative = Senti_negative.index(term_corona)
            index_gefunden_negative.append(index_negative)
       
# Die Liste mit Index-Verweisen durchgehen und den jeweiligen
# im Deskriptor erhöhen.
for index_normal, index_diskreptor in enumerate(index_gefunden_normal):
    current_value = deskriptor_normalzeit[0,index_diskreptor]
    deskriptor_normalzeit[0,index_diskreptor] = current_value + 1
    
for index_vorkrise, index_diskreptor in enumerate(index_gefunden_vorkrise):
    current_value = deskriptor_vorkrisenzeit[0,index_diskreptor]
    deskriptor_vorkrisenzeit[0,index_diskreptor] = current_value + 1
    
for index_positive, index_diskreptor in enumerate(index_gefunden_positive):
    current_value = deskriptor_Senti_positive[0,index_diskreptor]
    deskriptor_Senti_positive[0,index_diskreptor] = current_value + 1

for index_negative, index_diskreptor in enumerate(index_gefunden_negative):
    current_value = deskriptor_Senti_negative[0,index_diskreptor]
    deskriptor_Senti_negative[0,index_diskreptor] = current_value + 1
  
del index_negative, index_normal, index_positive, index_vorkrise
del index_gefunden_negative, index_gefunden_normal, index_gefunden_positive, index_gefunden_vorkrise
del current_value, index_diskreptor, term_corona, text, liste
  
# %%
"""
Nun erstellen wir ein großes Gesamt Dataframe mit dem vorkommen der Wörter sortiert
nach der jeweligen Art, also Normalzeit, Vorkrisenzeit etc.
"""

# Wir erstellen Dataframes auch für Positive und Negative Wörter um diese
# dann besser im df_gesamt hinzuzufügen.
df_positive = pd.DataFrame({'Terms':Senti_positive, 'Anzahl': 0,"Art":"Positive","ArtNr":3})

df_negative = pd.DataFrame({'Terms':Senti_negative, 'Anzahl': 0,"Art":"Negative","ArtNr":4})

df_gesamt = pd.concat([df_vorkrisenzeit, df_normalzeit, df_positive, df_negative], ignore_index=True, sort=True)

# Die Anzahl also Vorkommen nach Art im Dataframe einfügen. Der Wert wird dabei
# aus dem Deskriptor genommen.
for index in range(len(df_gesamt)):
    if (df_gesamt.at[index,'Art'] == "Vorkrisenzeit"):
        df_gesamt.at[index, 'Anzahl'] = deskriptor_vorkrisenzeit[0,index]          
    if (df_gesamt.at[index,'Art'] == "Normalzeit"):
        df_gesamt.at[index, 'Anzahl'] = deskriptor_normalzeit[0,index - len(df_vorkrisenzeit)]
    if (df_gesamt.at[index,'Art'] == "Positive"):
        df_gesamt.at[index, 'Anzahl'] = deskriptor_Senti_positive[0,index - (len(df_normalzeit) + len(df_vorkrisenzeit))]
    if (df_gesamt.at[index,'Art'] == "Negative"):
        df_gesamt.at[index, 'Anzahl'] = deskriptor_Senti_negative[0,index - (len(df_normalzeit) + len(df_vorkrisenzeit) + len(df_positive))]

df_gesamt = df_gesamt.sort_values(["Anzahl"], ascending = [False])

del index

# %%

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

X1 = df_gesamt[['Anzahl' , 'ArtNr']].iloc[: , :].values
inertia = []
for n in range(1 , 11):
    algorithm = (KMeans(n_clusters = n ,init='k-means++', n_init = 10 ,max_iter=300, 
                        tol=0.0001,  random_state= 111  , algorithm='elkan') )
    algorithm.fit(X1)
    inertia.append(algorithm.inertia_)

algorithm = (KMeans(n_clusters = 4 ,init='k-means++', n_init = 10 ,max_iter=300, 
                        tol=0.0001,  random_state= 111  , algorithm='elkan') )
algorithm.fit(X1)
centroids2 = algorithm.cluster_centers_

#Hier fügen wir dem dataframe die jeweilige Clusternummer zu
df_gesamt["Cluster"] = algorithm.labels_

import numpy as np

plt.figure(1 , figsize = (15 ,6))
plt.plot(np.arange(1 , 11) , inertia , 'o')
plt.plot(np.arange(1 , 11) , inertia , '-' , alpha = 0.5)
plt.xlabel('Number of Clusters') , plt.ylabel('Inertia')
plt.show()

# %%
"""
Fehlerabfrage
"""

print ("Check Diskreptor Normal: ", deskriptor_normalzeit.sum())

print ("Check Diskreptor Vorkrise: ", deskriptor_vorkrisenzeit.sum())

print ("Check Diskreptor Senti Positive: ", deskriptor_Senti_positive.sum())

print ("Check Diskreptor Senti Negative: ", deskriptor_Senti_negative.sum())

# %%
"""
Histogram für die beiden Zeiten
"""



# df_vorkrisenzeit.plot(kind='scatter',x='Terms',y='Anzahl',color='red')
# plt.show()


    
    
    
    
    
    
    
    
    
    
    