import finpie
import numpy as np
import urllib.request

year = 2020
copy = 1
startPos = 0
stopPos = 1000
new = 1 #set to zero for all subsequent runs
max_errors = 15 #how many errors in a row before program thinks it's a connection problem

text_path = f"Texts\\"
save_path = f"Data\\"
invalid = np.loadtxt(text_path+"No Download.txt",dtype='str')
posFile = f"Ticker Position {copy}.txt" #keeps track of the Symbol index for the current ticker whose data is being downloaded

Symbols = np.loadtxt(text_path+"YF Tickers Filtered.txt",dtype='str')

if not new:
    with open(text_path+posFile,'r') as f:
        startPos = int(f.readline().strip())

Symbols = Symbols[startPos:stopPos]

def getData(ticker,s_type,save_path,copy):
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
    
    df.to_csv(save_path+f'{s_type.capitalize()}{copy}\{ticker}_{s_type}.csv')
    return 1

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

valErrors = 0
for i,ticker in enumerate(Symbols):
    print(f'Getting data for {i+1} of {len(Symbols)} ({ticker}):')
    with open(text_path+posFile,'w') as f:
        f.write(str(startPos+i))

    if not ticker in invalid:
        result1 = getData(ticker,"cashflow",save_path,copy)
        if result1==3:
            valErrors+=1
            if valErrors>=max_errors:
                with open(text_path+posFile,'w') as f:
                    f.write(str(startPos+i+1-max_errors)) #max_errors start counting at 1 while startPos is zero indexed
                print("Too many tickers unable to be imported to pandas, check your internet connection!")
                exit()
        else:
            valErrors = 0

        if result1==1: #first retrieval succeeded
            result2 = getData(ticker,"income",save_path,copy)
    else:
        print(f"Skipped {ticker} due to it being on the invalid tickers list.")
    
print("Done!")
