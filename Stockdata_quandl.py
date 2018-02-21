# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 12:40:34 2017

@author: Rohan.Joseph
"""

# Import modules
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import datetime
import csv
import requests
import pandas_datareader.data as web
import pandas_datareader as pdr
from pandas_datareader import data, wb

# Input Start and End Date
start = datetime.datetime(2017,10,27)
end = datetime.datetime(2017,12,1)

Today = datetime.datetime.now().strftime ("%Y-%m-%d")

# Import list of stock names from NSE website
with requests.Session() as s:
    download = s.get('https://www.nseindia.com/products/content/sec_bhavdata_full.csv')
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = pd.DataFrame(list(cr))

# Clean the downloaded data
# Rename the headers
new_header = my_list.iloc[0] #grab the first row for the header
my_list = my_list[1:] #take the data less the header row
my_list = my_list.rename(columns = new_header)

# Get only the list of stock names - remove everything else
my_list['stock_name'] = "NSE/"+ my_list['SYMBOL']
stock_list = my_list['stock_name'].tolist()
stock_list = list(set(stock_list))

# Create Empty Dataframe
stock_final = pd.DataFrame()

# Scrape the stock prices from quandl
for i in range(len(stock_list)) :  
    print(i)    
    try:
        stock=[]
        stock = web.DataReader(stock_list[i],"quandl",start,end)
        stock['Name']=stock_list[i]
        
        stock_final = pd.DataFrame.append(stock_final,stock)
    except Exception: # Replace Exception with something more specific.
        i = i+1

# Download the appended stock prices
stock_final.to_csv('stockfinal_'+Today+'.csv')


#Getting min and max dates
date = stock_final.index.to_series()
max_date = max(date)
min_date = min(date)

stock_final['max_date'] = max_date
stock_final['min_date'] = min_date
stock_final['date'] = date

#Subset dataset only for first and last date
stock_required = stock_final.query('date==max_date | date==min_date')

#Sort data
stock_required = stock_required.sort_values(['Name','date'])

#Lag of Close Price and date
stock_required['Prev_Close'] = stock_required.Close.shift(+1)
stock_required['Prev_date'] = stock_required.date.shift(+1)

#Remove unwanted rows
stock_required = stock_required.query('date==max_date')

#Remove unwanted columns
stock_required.drop('min_date',axis=1,inplace=True)
stock_required.drop('max_date',axis=1,inplace=True)

# Percentage difference of Close Prices
stock_required['Perc_diff'] = (stock_required['Close']-stock_required['Prev_Close'])/(stock_required['Prev_Close'])

#Keep only required price range of stocks
stock_final = stock_required.query('Close>20 & Close<250 & Perc_diff>0')

#Keep only the top 5 percentile based on percentage difference
thestocks = pd.DataFrame(stock_final[stock_final.Perc_diff > stock_final.Perc_diff.quantile(.95)])
thestocks = thestocks.sort_values('Perc_diff',ascending = False)

# Download stock data  
thestocks.to_csv('thestocks_'+Today+'.csv',index=False)

