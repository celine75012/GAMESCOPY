#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

print_ = print

DEBUG = False


def print(*args, **kwargs):
    if DEBUG:
        print_(*args, **kwargs)

import pandas as pd
import os
os.chdir('c:\\Users\\celine\\Desktop')
data = pd.read_csv('all_games.csv')


#print(data)

data["Classification"] = pd.Series(lambda: None)

#print(data)

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
}

for i, row in tqdm(data.iterrows(), total=len(data)):
    
#sauvegarde automatique (pas necessaire)   
     if i != 0 and i%50 == 0:
        print_("backuping data at row", str(i)+"...")
        data.to_csv("video_games_classed.csv")
    #print(i)
    #print("waw")
    #print(row["Title"])
     if not pd.isnull(row.Classification):
            continue
#if __name__ == "__main__":
name = row["Classification"]
    # Make a request to the PEGI website to get the HTML for the page
url = f'https://pegi.info/search-pegi?q={name}'
    #print(url)
response = requests.get(url, headers=headers)

    # Parse the HTML of the page
soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element that contains the age rating
balise = None
print("SEARCHING :", name)
   
try:
    balise = soup.select(
        'div.body.text-with-summary > article:nth-child(1) > div.game-content > div.description > div.age-rating > img'
        )[0]
except IndexError:
        print("ERR : Can't find the pegi")
# Extract the age rating from the element
age = 'NA'
match = False
try:
    if balise is not None:
        match = re.search(r'(\d+)\.png', balise["src"])
    if match:
        age = int(match.group(1))
except ValueError:
    print("ERR : age found was not a number")
except IndexError:
    print("ERR : image didn't have source")

    #print(age)
data.loc[i, "Classification"] = age
print(f'SUCCESS : The age rating for {name} is: {age}')

print_(data)
data.to_csv("video_games_classed.csv")


# In[ ]:




