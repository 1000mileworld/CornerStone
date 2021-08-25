from os import listdir
from os.path import isfile, join
import requests
import numpy as np
import time

year = 2020

origin_path = f"..\Data\Prices\{year}\\"
statements_path = "Data\\"
text_path = "Texts\\"
base_url = "https://www.macrotrends.net/stocks/charts/"
outfile = text_path+"Missing Symbols.txt"
invalid = np.loadtxt(text_path+"No Download.txt",dtype='str')

s_origin = [f.split('.')[0] for f in listdir(origin_path) if isfile(join(origin_path, f))]
s_cashflow = [f.split('_')[0] for f in listdir(statements_path+"Cashflow") if isfile(join(statements_path+"Cashflow", f))]
s_income = [f.split('_')[0] for f in listdir(statements_path+"Income") if isfile(join(statements_path+"Income", f))]

def compare(s_origin,s_compare,outfile):
    s_missing = []
    for ticker in s_origin:
        if not ticker in s_compare:
            s_missing.append(ticker)
    return s_missing

def saveArray(arr,outfile):
    arr_np = np.array(arr)
    with open(outfile, 'w'):
        np.savetxt(outfile,arr_np,fmt='%s')
    #loaded = np.loadtxt(outfile,dtype='str')
    #print(loaded.tolist())

def get_url(url):
    for x in range(0, 5):  # try 5 times
        try:
            response = requests.get(url)
            break
        except:
            print(f"Retrying ({x+1})...")
            time.sleep(5)

    return response

s_missing = compare(s_origin,s_income,outfile)
s_missing = s_missing[563:]
has_url = []
for i,ticker in enumerate(s_missing):
    print(f'Checking ticker {i+1} of {len(s_missing)} ({ticker})...')
    if not ticker in invalid:
        url = base_url+ticker
        response = get_url(url)
        if response.history:
            # Request was redirected, status code 301
            with open(outfile,'a+') as f:
                f.write(f"{ticker}\n")
            has_url.append(ticker)
            #print(response.url)

print(has_url)
#saveArray(has_url,outfile)