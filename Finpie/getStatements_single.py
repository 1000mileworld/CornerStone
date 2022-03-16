import finpie
import numpy as np
import urllib.request
import time
from datetime import date
import os

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

def writeLog(file,mode,text):
    with open(file,mode) as f:    
        f.write(text)

def getTimeStr():
    today = date.today()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return f"{today} {current_time} local time:"


copy = 6

max_errors = 257 #how many errors in a row before program thinks it's a connection problem

text_path = f"Texts\\"
save_path = f"Data\\"
invalid = np.loadtxt(text_path+"No Download.txt",dtype='str')
pos_file = f"Ticker Position {copy}.txt" #keeps track of the Symbol index for the current ticker whose data is being downloaded
log_file = f"Log {copy}.txt"

#print("Verifying internet connection...")
#time.sleep(10)
time_str = getTimeStr()
if not connect():
    writeLog(text_path+log_file,'a',f"{time_str} script unable to start due to no internet connection\n")
    exit()
writeLog(text_path+log_file,'a',f"{time_str} script started\n")

with open(text_path+pos_file,'r') as f:
    startPos = int(f.readline().strip())


#Symbols = np.loadtxt(text_path+"YF Tickers Filtered.txt",dtype='str').tolist()
Symbols = np.loadtxt(text_path+"Missing Symbols.txt",dtype='str').tolist()
#Symbols = Symbols[startPos:]

valErrors = 0
for i,ticker in enumerate(Symbols):
    print(f'Getting data for {i+1} of {len(Symbols)} ({ticker})')
    writeLog(text_path+pos_file,'w',str(startPos+i))
    if not ticker in invalid:
        result1 = getData(ticker,"cashflow",save_path,copy)
        if result1==3:
            valErrors+=1
            if valErrors>=max_errors:                
                print("Too many tickers unable to be imported to pandas, checking internet connection...")
                if not connect():
                    print("No internet connection found, system restarting in 30 seconds...")
                    writeLog(text_path+pos_file,'w',str(startPos+i+1-max_errors)) #max_errors start counting at 1 while startPos is zero indexed                       
                    time_str = getTimeStr()
                    writeLog(text_path+log_file,'a',f"{time_str} PC restarted\n")
                    os.system("shutdown /r /t 30")
                elif not connect(host="https://www.macrotrends.net/"):
                    print("Internet connection verified, but no connection received from Macrotrends.")
                    time_str = getTimeStr()
                    writeLog(text_path+log_file,'a',f"{time_str} script exited due to no connection from Macrotrends\n")
                    exit()
                else:
                    print("Internet connection verified, increasing max errors allowed by 5.")
                    max_errors+=5
        else:
            valErrors = 0

        if result1==1: #first retrieval succeeded
            result2 = getData(ticker,"income",save_path,copy)
    else:
        print(f"Skipped {ticker} due to it being on the invalid tickers list.")
    
print("Done!")
time_str = getTimeStr()
writeLog(text_path+log_file,'a',f"{time_str} script finished\n")
