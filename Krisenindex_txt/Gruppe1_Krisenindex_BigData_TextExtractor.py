# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:34:00 2020

@author: Gruppe
"""

# %%
#Gathering Data

# %%
#dataframe(?)

# %%
#spacy


# %%
#string to txt

#Platzhalter für die späteren Artikeltexte
Artikeltexte = ['aba', 'xyz', 'xgx', 'dssd', 'sdjh']

for x in range(0,len(Artikeltexte)):
       filename = "Artikeltext%d.txt" % (x)
       writeFile = open(filename, 'w')
       writeFile.write(Artikeltexte[x])
       writeFile.close()

# %%
