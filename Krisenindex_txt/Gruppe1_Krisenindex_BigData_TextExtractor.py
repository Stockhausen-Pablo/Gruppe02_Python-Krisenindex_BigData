# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:34:00 2020

@author: Gruppe 2
"""

import spacy
from spacy_langdetect import LanguageDetector
from bs4 import BeautifulSoup
import requests
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
nlp = spacy.load("de_core_news_md")
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
nlp_e = spacy.load("en_core_web_sm")
stamm = "https://www.spiegel.de/nachrichtenarchiv/artikel-"
tag = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
schaltjahre = [2000, 2004, 2008, 2012, 2016, 2020]
tags_d = ["NN", "NE", "NNE", "ADJA", "ADJD", "VVINF", "VVIMP"]
tags_e = ["NN", "NNP", "NNPS", "NNS","JJ", "JJR", "JJS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

def output(text, x, ordner_path):
    if x < 9:
        filename = ordner_path + "/Artikeltext0%d.txt" % (x+1)
    else:
        filename = ordner_path + "/Artikeltext%d.txt" % (x+1)            
    writeFile = open(filename, 'w', encoding="utf-8")
    writeFile.write(text)
    writeFile.close()
    
def gathering(monat, jahr, anzahl, x):
    if x == 'k':
        ordner_path = dir_path + "/Krise/" + jahr + "_" + monat
    elif x == 'n':
        ordner_path = dir_path + "/Normal/" + jahr + "_" + monat
    if not os.path.exists(ordner_path):
        os.makedirs(ordner_path)
    counter = 0
    links_monat = []
    links_artikel= []
    Artikeltexte = [] 
    if monat == "01" or monat == "03" or monat == "05" or monat == "07" or monat == "08" or monat == "10" or monat == "12":
        for i in range(len(tag)):
            link = stamm + tag[i] + "." + monat + "." + jahr + ".html"
            links_monat.append(link)
    elif monat =="02":
        if int(jahr) in schaltjahre:
            for i in range(len(tag)-2):
                link = stamm + tag[i] + "." + monat + "." + jahr + ".html"
                links_monat.append(link)
        else: 
            for i in range(len(tag)-3):
                link = stamm + tag[i] + "." + monat + "." + jahr + ".html"
                links_monat.append(link)
    else:
        for i in range(len(tag)-1):
            link = stamm + tag[i] + "." + monat + "." + jahr + ".html"
            links_monat.append(link)
    
    for i in links_monat:
        soup = BeautifulSoup(requests.get(i).content, 'html.parser')
        
        for a in soup.select("article>header>h2>a"):
            links_artikel.append(a['href'])
           
    for artikel in links_artikel:
        try:
            soup_link = BeautifulSoup(requests.get(artikel).content, 'html.parser')
            text = ""
            for i in soup_link.select("section p", text=True):    
                text = text + i.text

            doc = nlp(text)
            if doc._.language["language"] == "en":
                doc = nlp_e(text)
                tags = tags_e.copy()
            else:
                tags = tags_d.copy()            
            s = ""
            for token in doc:
                if token.tag_ in tags:    
                    s = s + " " + token.lemma_  
            if len(s) !=0:                                                  
                Artikeltexte.append(s)
                output(s, counter, ordner_path)
                counter += 1
                if counter == anzahl:
                    break         
        except:
            pass
    return Artikeltexte
    
Artikeltexte = gathering("09", "2009", 10, "k")
# %%
#dataframe(?)

# %%
#spacy


# %%
#string to txt

#Platzhalter für die späteren Artikeltexte
#Artikeltexte = ['aba', 'xyz', 'xgx', 'dssd', 'sdjh']

#for x in range(0,len(Artikeltexte)):
       #filename = "Artikeltext%d.txt" % (x)
       #writeFile = open(filename, 'w')
       #writeFile.write(Artikeltexte[x])
       #writeFile.close()

# %%
