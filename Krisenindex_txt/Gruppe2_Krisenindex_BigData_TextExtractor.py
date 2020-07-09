# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:34:00 2020

@author: Gruppe
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
tags_d = ["NN", "NE", "NNE", "ADJA", "ADJD"]
tags_e = ["NN", "NNP", "NNPS", "NNS", "JJ", "JJR", "JJS"]

def output(text, x, ordner_path):
    filename = ordner_path + "/Artikeltext%d.txt" % (x+1)            
    writeFile = open(filename, 'w')
    writeFile.write(text)
    writeFile.close()
    
def gathering_2019(anzahl, start):
    counter = 0
    links_monat = []
    Artikeltexte = [] 
    monate = tag[:12]
    
    for monat in monate:
        
        if monat == "01" or monat == "03" or monat == "05" or monat == "07" or monat == "08" or monat == "10" or monat == "12":
            for i in range(len(tag)):
                link = stamm + tag[i] + "." + monat + ".2019.html"
                links_monat.append(link)
        elif monat =="02":
            for i in range(len(tag)-3):
                link = stamm + tag[i] + "." + monat + ".2019.html"
                links_monat.append(link)
        else:
            for i in range(len(tag)-1):
                link = stamm + tag[i] + "." + monat + ".2019.html"
                links_monat.append(link)
                
    links_monat = links_monat[start:]  
          
    for index, link in enumerate(links_monat):
        index += start
        nummer = str(index + 1)
        links_tag = []
        soup = BeautifulSoup(requests.get(link).content, 'html.parser')
        if index < 99:
            if index < 9:
                ordner_path = dir_path + "/Corona/00" + nummer
            else:
                ordner_path = dir_path + "/Corona/0" + nummer
        else:
            ordner_path = dir_path + "/Corona/" + nummer
        if not os.path.exists(ordner_path): 
            os.makedirs(ordner_path)
        for a in soup.select("article>header>h2>a"):
            if '/politik/' in a['href']:
                links_tag.append(a['href'])
           
        for artikel in links_tag:
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
            
        print("2019: Tag " + str(index + 1) + " von 365") 
        
    return Artikeltexte    

#gathering_2019(0, 0)

## %%

def gathering_2020(anzahl, start):
    counter = 0
    links_monat = []
    Artikeltexte = [] 
    monate = tag[:3]
    
    for monat in monate:
        
        if monat == "01" or monat == "03": 
            for i in range(len(tag)):
                link = stamm + tag[i] + "." + monat + ".2020.html"
                links_monat.append(link)
        elif monat =="02":
            for i in range(len(tag)-2):
                link = stamm + tag[i] + "." + monat + ".2020.html"
                links_monat.append(link)
        else:
            for i in range(len(tag)-1):
                link = stamm + tag[i] + "." + monat + ".2020.html"
                links_monat.append(link)
                
    links_monat = links_monat[start:]  
          
    for index, link in enumerate(links_monat):
        index += start
        nummer = str(index + 1)
        links_tag = []
        soup = BeautifulSoup(requests.get(link).content, 'html.parser')
        if index < 99:
            if index < 9:
                ordner_path = dir_path + "/Corona/x20_00" + nummer
            else:
                ordner_path = dir_path + "/Corona/x20_0" + nummer
        else:
            ordner_path = dir_path + "/Corona/x20_" + nummer
        if not os.path.exists(ordner_path): 
            os.makedirs(ordner_path)
        for a in soup.select("article>header>h2>a"):
            if '/politik/' in a['href']:
                links_tag.append(a['href'])
           
        for artikel in links_tag:
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
            
        print("2020: Tag " + str(index +  1) + " von 91")
        
    return Artikeltexte   

#gathering_2020(0,0)

##%%

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
            if '/politik/' in a['href']:
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
                print(jahr + "-" + monat + ": Artikel " + str(counter) + " von " + str(len(links_artikel)))
                if counter == anzahl:
                    break         
        except:
            pass
        
    return Artikeltexte

#gathering("08", "2008", 0, "k")
#gathering("09", "2008", 0, "k")
#gathering("10", "2008", 0, "k")
#gathering("12", "2009", 0, "k")
#gathering("01", "2010", 0, "k")
#gathering("02", "2010", 0, "k")
#gathering("06", "2014", 0, "k")
#gathering("07", "2014", 0, "k")
#gathering("08", "2014", 0, "k")
#gathering("07", "2015", 0, "k")
#gathering("08", "2015", 0, "k")
#gathering("09", "2015", 0, "k")

# gathering("05", "2008", 0, "n")
# gathering("06", "2008", 0, "n")
# gathering("12", "2014", 0, "n")
# gathering("01", "2015", 0, "n")
# gathering("07", "2018", 0, "n")
# gathering("08", "2018", 0, "n")
# gathering("07", "2019", 0, "n")
# gathering("08", "2019", 0, "n")
