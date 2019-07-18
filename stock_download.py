import pandas as pd
import numpy as np
from yahoo_historical import Fetcher

#list of equity symbols from NASDAQ
url1="https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download"
data1=pd.read_csv(url1)

#list of equity symbols from NYSE
url2="https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download"
data2=pd.read_csv(url2)

#List of tickers
Symbols = data1['Symbol'].append(data2['Symbol']).drop_duplicates()

#Calculate time for run
import time
t0 = time.time()

# Create Empty Dataframe
stock_final = pd.DataFrame()

#loop through each ticker and download
for i in Symbols:  
    print(i, sep=',', end=',', flush=True)  
    try:
        stock = []
        data = Fetcher(i, [2019,5,16], [2019,7,16])
        stock = data.getHistorical()
        
        if len(stock) == 0:
            None
        else:
            stock['Name']=i
            stock_final = stock_final.append(stock,sort=False)
    except Exception: # Replace Exception with something more specific.
        None
        
t1 = time.time()

#total time taken
total = t1-t0
