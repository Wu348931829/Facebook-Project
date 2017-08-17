
# coding: utf-8

# In[136]:

import requests
import urllib.request
import json
import datetime
import csv
import time
import pandas as pd
import numpy as np
from random import randint
from time import sleep

df = pd.read_csv('Search Result From FB remove NA.csv',encoding='latin-1')


# In[141]:

df['City'] = ' '
df['State'] = ' '
df['Address'] = ' '
df['Zip'] = ' '
df['Url'] = ' '
df['Facebook ID'].apply(str)

app_id = "id"
app_secret = "secret" 
access_token = app_id + "|" + app_secret

access_token = ""  

base = "https://graph.facebook.com/v2.10"
df['Url'] = base + "/"  + df['Facebook ID'] +'?fields=location&access_token=' + access_token


# In[143]:

for i in range(len(df['Url'])):
    r = requests.get(df['Url'][i])
    if r.status_code != 400:
        data = json.loads(r.text)
        if data.get('location') is not None:
            if data['location'].get('city') is not None:
                df['City'][i] = data['location']['city']
            if data['location'].get('state') is not None:
                df['State'][i] = data['location']['state']
            if data['location'].get('street') is not None:
                df['Address'][i] = data['location']['street']
            if data['location'].get('zip') is not None:
                df['Zip'][i] = data['location']['zip']
        else:
            df['City'][i] = 'NA'
            df['State'][i] = 'NA'
            df['Address'][i] = 'NA'
            df['Zip'][i] = 'NA'
    time.sleep(2)


# In[145]:

df.to_csv('3.csv')

