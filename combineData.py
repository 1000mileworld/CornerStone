import pandas as pd
from os import listdir
from os.path import isfile, join
from IPython.display import display

year = 2015
load_path = f"Data\Reports Parsed\{year}\\"
save_path = "Data\Conglomerate\\"

income_headers = ['Ticker','Shares (Basic)','Shares (Diluted)','Revenue','Cost of Revenue','Gross Profit','Operating Expenses','Selling, General & Administrative','Research & Development','Depreciation & Amortization',
'Operating Income (Loss)','Non-Operating Income (Loss)','Interest Expense, Net','Pretax Income (Loss), Adj.','Abnormal Gains (Losses)','Pretax Income (Loss)','Income Tax (Expense) Benefit, Net',
'Income (Loss) from Continuing Operations','Net Extraordinary Gains (Losses)','Net Income','Net Income (Common)']

files = listdir(load_path)
files = files[:4]

def parse_income(headers,ticker,df):
    multiplier = 1

    if 'THOUSANDS' in df.columns[0].upper():
        multiplier = 1e3
    elif 'MILLION' in df.columns[0].upper():
        multiplier = 1e6
    else:
        raise Exception(f'Cannot determine multiplier: {df.columns[0].upper()}')

    display(df)

for i, file in enumerate(files):
    print(f'Parsing {i+1} of {len(files)} files: '+file)
    if isfile(join(load_path,file)):
        ticker = file.split('.')[0].split('_')[0]
        type = file.split('.')[0].split('_')[1]
        df = pd.read_csv(load_path+file)
        if type=='income':
            parse_income(income_headers,ticker,df)