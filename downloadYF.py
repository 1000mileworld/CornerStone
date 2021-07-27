import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io
import json

year = 2015

startDate = datetime.datetime(year,1,1)
endDate = datetime.datetime(year+1,1,1)

root = 'D:\Joe\Investing\Algo Trading\Python\CornerStone'

# url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
# s = requests.get(url).content
# companies = pd.read_csv(io.StringIO(s.decode('utf-8')))

nasdaq = pd.read_csv("nasdaq_screener.csv")
Symbols = nasdaq['Symbol'].tolist()
#Symbols = Symbols[302:]

#Symbols = ['AKO/A','AAPL']

for i,symbol in enumerate(Symbols):  
    
    print(f'Downloading stock {i+1} of {len(Symbols)} ({symbol})')

    if not symbol.isalpha():
        print(f'Skipping {symbol}: symbol contains nonalpha characters')
        continue

    stock = yf.Ticker(symbol)
    if stock.info['regularMarketPrice']==None:
        print(f'No price info found for {symbol}')
    else:
        hist = yf.download(symbol,start=startDate,end=endDate,progress=False)
        if len(hist)!=0:
            hist.to_csv(f'{root}\Data\Prices\{year}\{symbol}.csv')

    time.sleep(2)

print("Download complete!")