
# coding: utf-8

# In[ ]:

# import libraries
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

df = pd.read_csv('Sample_20.csv')

del df['BusinessId']
del df['ListingId']
del df['Unnamed: 0']
del df['LoanAmt']
del df['Indeterminate']
del df['nowFraud']

df['BusinessName'] = df['BusinessName'].str.strip()
df['BusinessName'] = df['BusinessName'].str.replace(' ', '%')
df['BusinessName'] = df['BusinessName'].str.replace('!', '')
df['BusinessName'] = df['BusinessName'].str.replace("'", '%')
df['BusinessName'] = df['BusinessName'].str.replace("#", '%')
df['BusinessName'] = df['BusinessName'].str.strip()

df['Url'] = ' '
df['Facebook ID'] = ' '
df['Facebook Search Result'] = ' '

# apply for Graph API from Facebook
app_id = "Input your ID here"
app_secret = "Input you secret here" # DO NOT SHARE WITH ANYONE!
# access_token = app_id + "|" + app_secret

access_token = "Input your token here"
# Token expire every two hours

df['Url'] = base + "/" + "search?q=" + df['BusinessName'] +'&type=page&access_token=' + access_token

# Get Facebook search result and Facebook ID
for i in range(len(df['Url'])):
    if len(df['BusinessName'][i]) > 0:
        req = urllib.request.Request(df['Url'][i])
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        if len(data['data']) > 0:
            df['Facebook ID'][i] = data['data'][0]['id']
            df['Facebook Search Result'][i] = data['data'][0]['name']
        else:
            df['Facebook ID'][i] = 'NA'
            df['Facebook Search Result'][i] = 'NA'
    else:
        df['Facebook ID'][i] = 'NA'
        df['Facebook Search Result'][i] = 'NA'
    time.sleep(2)



# In[ ]:

df


# In[ ]:

df.to_csv('11.csv')

