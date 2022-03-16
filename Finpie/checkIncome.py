# get missing income statements based on downloaded cashflow statements

import finpie
from os import listdir
from os.path import isfile, join
import time

max_retries = 5
delay = 30
save_path = f"Data\\Income\\"
statements_path = f"Data\\"
s_cashflow = [f.split('_')[0] for f in listdir(statements_path+"Cashflow") if isfile(join(statements_path+"Cashflow", f))]
s_income = [f.split('_')[0] for f in listdir(statements_path+"Income") if isfile(join(statements_path+"Income", f))]

def findMissing(s_origin,s_compare):
    s_missing = []
    for ticker in s_origin:
        if not ticker in s_compare:
            s_missing.append(ticker)
    return s_missing

def getIncomeData(ticker,s_type,save_path):
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
    
    df.to_csv(save_path+f'{ticker}_{s_type}.csv')
    return 1
    
Symbols = findMissing(s_cashflow,s_income)
for i,ticker in enumerate(Symbols):
    print(f'Getting data for {i+1} of {len(Symbols)} ({ticker}):')

    result = getIncomeData(ticker,"income",save_path)
    counter = 0
    while result==3: #if value error, give several retries
        counter+=1
        if counter>max_retries:
            print("Max retries reached, unable to download.")
            break
        else:
            print(f'Retrying {counter} of {max_retries} times, waiting {delay} seconds...')
            time.sleep(delay)
            getIncomeData(ticker,"income",save_path)

print("Done!")
