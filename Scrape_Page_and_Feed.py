
# coding: utf-8

# In[ ]:

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


# In[ ]:

# ww: update at 8/8 - more than one page problem solved
df = pd.read_csv('not conservative matching.csv',encoding='latin-1')
df1 = pd.read_csv('Search Result From FB remove NA - Copy.csv',encoding='latin-1')

result = pd.merge(df,df1,on = 'LeadId', how = 'inner')

del result['Unnamed: 0_x']
del result['Unnamed: 0_y']
del result['everBad_y']
del result['BusinessName_y']
del result['City.x']
del result['State.x']
del result['Zip.x']
del result['Address']
del result['index']
del result['Unnamed: 17']
del result['namedist']
del result['adddist']
del result['Address2']

app_id = "id"
app_secret = "secret" 
access_token = app_id + "|" + app_secret

access_token = ""  

base = "https://graph.facebook.com/v2.10"
result['Url'] = base + "/"  + result['Facebook ID'] +'?fields=checkins%2Ctalking_about_count%2Cfan_count%2Cfounded%2Cis_permanently_closed%2Coverall_star_rating%2Crating_count%2Cengagement&access_token=' + access_token

# Scrape Page
result['checkins'] = ' '
result['fan_count'] = ' '
result['rating_count'] = ' '
result['talking_about_count'] = ' '
result['is_permanently_closed'] = ' '
result['engagement'] = ' '
result['star_rating'] = ' '

for i in range(len(result['Url'])):
    r = requests.get(result['Url'][i])
    if r.status_code != 400:
        data = json.loads(r.text)
        if data.get('checkins') is not None:
            result['checkins'][i] = data['checkins']
        if data.get('fan_count') is not None:
            result['fan_count'][i] = data['fan_count']
        if data.get('rating_count') is not None:
            result['rating_count'][i] = data['rating_count']
        if data.get('talking_about_count') is not None:
            result['talking_about_count'][i] = data['talking_about_count']
        if data.get('is_permanently_closed') is not None:
            result['is_permanently_closed'][i] = data['is_permanently_closed']
        if data.get('star_rating') is not None:
            result['star_rating'][i] = data['star_rating']
        if data.get('engagement') is not None:
            result['engagement'][i] = data['engagement']['count']
        else:
            result['checkins'][i] = 'NA'
            result['fan_count'][i] = 'NA'
            result['rating_count'][i] = 'NA'
            result['talking_about_count'][i] = 'NA'
            result['is_permanently_closed'][i] = 'NA'
            result['star_rating'][i] = 'NA'
            result['engagement'][i] = 'NA'

    time.sleep(2)


# In[ ]:

# result.to_csv('FB result 1.csv')


# In[ ]:

# result = pd.read_csv('Feed - Copy.csv',encoding='latin-1')


# In[ ]:

# Scrape Feed (Posting)
result = pd.read_csv('Feed - Copy.csv',encoding='latin-1')
result['Facebook ID'] = result['Facebook ID'].apply(str)

app_id = ""
app_secret = "" 
access_token = app_id + "|" + app_secret

access_token = ""  

base = "https://graph.facebook.com/v2.10"
result['Url'] = base + "/"  + result['Facebook ID'] +'/feed?access_token=' + access_token

result['Number_of_post'] = 0
result['Created_time'] = ' '

for i in range(len(result['Url'])):
    r = requests.get(result['Url'][i])
    if r.status_code != 400:
        data = json.loads(r.text)
        has_next_page = True
        while has_next_page:
            if data.get('data') is not None:
                result['Number_of_post'][i] = len(data['data']) + result['Number_of_post'][i]
                if data['data'] != []:
                    if data['data'][len(data['data'])-1]['created_time'] is not None:
                        result['Created_time'][i] = data['data'][len(data['data'])-1]['created_time']

            else:
                result['Number_of_post'][i] = 'NA'
                result['Created_time'][i] = 'NA'
            if data['data'] == []:
                break
            elif data['paging'].get('next') is not None:
                data = json.loads(requests.get(data['paging']['next']).text)
            else:
                has_next_page = False

    time.sleep(2)


# In[ ]:

#result.to_csv('Feed 3.csv')

