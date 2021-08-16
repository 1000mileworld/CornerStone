import pandas as pd
import yfinance as yf
import datetime
import time
from os import listdir
from os.path import isfile, join

year = 2020
load_path = f"..\Data\Prices\{year}\\"
save_path = f"..\Data\Prices\\2020 add on\\"

tickers_downloaded = [f.split('.')[0] for f in listdir(load_path) if isfile(join(load_path, f))]

startDate = datetime.datetime(year,1,1)
endDate = datetime.datetime(year+1,1,1)

nasdaq = pd.read_csv("tickers.csv")
Symbols = nasdaq['Symbol'].tolist()

Symbols = Symbols[3580:]

#Symbols = ['HMPT']

for i,ticker in enumerate(Symbols):  
    
    ticker = ticker.strip()
    print(f'Downloading stock {i+1} of {len(Symbols)} ({ticker})')

    if not ticker in tickers_downloaded:

        if not ticker.isalpha():
            print(f'Skipping {ticker}: symbol contains nonalpha characters')
            continue

        stock = yf.Ticker(ticker)
        if stock.info['regularMarketPrice']==None:
            print(f'No price info found for {ticker}')
        else:
            hist = yf.download(ticker,start=startDate,end=endDate,progress=False)
            if len(hist)!=0:
                hist.to_csv(save_path+f'{ticker}.csv')
    else:
        print(f'Price data for {ticker} already downloaded!')

    time.sleep(2)

print("Download complete!")