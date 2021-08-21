import finpie
from os import listdir
from os.path import isfile, join
import time
import numpy as np

year = 2020

load_path = f"..\Data\Prices\{year}\\"
save_path = f"Data\\"

Symbols = np.loadtxt("YF Tickers Filtered.txt",dtype='str')

#Symbols = [f.split('.')[0] for f in listdir(load_path) if isfile(join(load_path, f))]
#Symbols = Symbols[4063:4500]
#Symbols = ["OTRK"]

def getData(ticker,s_type,save_path):
    print(f"Downloading {s_type} statement...")

    fd = finpie.Fundamentals(ticker, source = 'macrotrends', freq = 'A')

    try:
        if s_type=="cashflow":
            df = fd.cashflow_statement()
        elif s_type=="income":
            df = fd.income_statement()
        else:
            print(f"Unrecognized statement type: {s_type}")
            return 2
    except ValueError:
        print("!!!-------------Unable to import data to pandas--------------!!!")
        return 3
    
    df.to_csv(save_path+f'{s_type.capitalize()}\{ticker}_{s_type}.csv')
    return 1
  
valErrors = 0
for i,ticker in enumerate(Symbols):
    print(f'Getting data for {i+1} of {len(Symbols)} ({ticker}):')
    
    result1 = getData(ticker,"cashflow",save_path)
    if result1==3:
        valErrors+=1
        if valErrors>15:
            print("Too many tickers unable to be imported to pandas, check your internet connection!")
            exit()
    else:
        valErrors = 0

    if result1==1: #first retrieval succeeded
        result2 = getData(ticker,"income",save_path)
        counter = 0
        while result2==3: #if value error, give several retries
            counter+=1
            if counter>2:
                print("Max retries reached, unable to download.")
                break
            else:
                time.sleep(5)
                print(f'Retrying ({counter})')
                getData(ticker,"income",save_path)
    
print("Done!")
