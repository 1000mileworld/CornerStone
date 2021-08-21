#filter tickers whose price was downloaded from yahoo finance
#only feed tickers to finpie whose price has all available data for the past year

from os import listdir
import numpy as np
import pandas as pd
#from IPython.display import display

year = 2020

outfile = "YF Tickers Filtered.txt"
load_path = f"..\Data\Prices\{year}\\"
ref = "AAPL.csv"

df_ref = pd.read_csv(load_path+ref)
trading_days = len(df_ref.index)

#display(data)
Symbols = []
for f in listdir(load_path):
    df = pd.read_csv(load_path+f)
    if len(df.index)>=trading_days*0.75: #will accept tickers with data for most of the year
        ticker = f.split('.')[0]
        Symbols.append(ticker)

Symbols_np = np.array(Symbols)
with open(outfile, 'w') as f:
    np.savetxt(outfile,Symbols_np,fmt='%s')