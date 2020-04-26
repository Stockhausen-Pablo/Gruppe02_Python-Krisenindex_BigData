# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:34:00 2020

@author: Gruppe
"""

# %%
#Gathering Data
import spacy
from bs4 import BeautifulSoup
import requests

nlp = spacy.load("de_core_news_md")  
stamm = "https://www.spiegel.de/nachrichtenarchiv/artikel-"
tag = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]

def gathering(monat, jahr, anzahl):
    counter = 0
    links_monat = []
    links_artikel= []
    text_gesamt_liste = [] 
    if monat == "01" or monat == "03" or monat == "05" or monat == "07" or monat == "08" or monat == "10" or monat == "12":
        for i in range(len(tag)):
            link = stamm + tag[i] + "." + monat + "." + jahr + ".html"
            links_monat.append(link)
    elif monat =="02":
        if int(jahr)==2000 or int(jahr)==2004 or int(jahr)==2008 or int(jahr)==2012 or int(jahr)==2016 or int(jahr)==2020:
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
    
        soup_link = BeautifulSoup(requests.get(artikel).content, 'html.parser')
        text = ""
        for i in soup_link.select("section p", text=True):    
            text = text + i.text
     
        doc = nlp(text)
        s = ""
        for token in doc:
            if token.tag_ == "NN" or token.tag_ == "NE" or token.tag_ == "NNE" or token.tag_  == "ADJA" or token.tag_  == "ADJD":    
                s = s + " " + token.lemma_                                                    
        text_gesamt_liste.append(s) 
        counter += 1
        if counter == anzahl:
            break         
    return text_gesamt_liste

Artikeltexte = gathering("09", "2009", 10)
# %%
#dataframe(?)

# %%
#spacy


# %%
#string to txt

#Platzhalter für die späteren Artikeltexte
#Artikeltexte = ['aba', 'xyz', 'xgx', 'dssd', 'sdjh']

for x in range(0,len(Artikeltexte)):
       filename = "Artikeltext%d.txt" % (x)
       writeFile = open(filename, 'w')
       writeFile.write(Artikeltexte[x])
       writeFile.close()

# %%
