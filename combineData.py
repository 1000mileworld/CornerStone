import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from IPython.display import display

year = 2015
load_path = f"Data\Reports Parsed\{year}\\"
save_path = "Data\Conglomerate\\"

#income_headers = ['Ticker','Shares (Basic)','Shares (Diluted)','Revenue','Cost of Revenue','Gross Profit','Operating Expenses','Selling, General & Administrative','Research & Development','Depreciation & Amortization',
#'Operating Income (Loss)','Non-Operating Income (Loss)','Interest Expense, Net','Pretax Income (Loss), Adj.','Abnormal Gains (Losses)','Pretax Income (Loss)','Income Tax (Expense) Benefit, Net',
#'Income (Loss) from Continuing Operations','Net Extraordinary Gains (Losses)','Net Income','Net Income (Common)']

income_headers = ['Revenue', 'Net Income']

files = listdir(load_path)
#files = files[35:36]
pos = files.index('ABC_income.csv')
files = files[pos:pos+1]

def parse_income(headers,ticker,df):
    
    report_name = df.columns[0].upper()
    labels = df[df.columns[0]].tolist()
    
    multiplier = 1
    if 'MILLIONS' in report_name:
        multiplier = 1e6
    elif 'THOUSANDS' in report_name:
        multiplier = 1e3
    #elif 'THOUSANDS' in report_name and 'MILLIONS' in report_name:
    #    raise Exception(f'Both THOUSANDS and MILLIONS present: {report_name}')
    elif not 'MILLIONS' in report_name and not 'THOUSANDS' in report_name:
        pass
    else:
        raise Exception(f'Cannot determine multiplier: {report_name}')

    arr = [ticker]
    for header in headers:
        if header=="Revenue":
            keywords = ['NET SALES','REVENUE']
        elif header=="Net Income":
            keywords = ['NET INCOME', 'NET EARNINGS', 'NET (LOSS) INCOME']

        found = False
        for label in labels:
            if isinstance(label, str) and any(keyword in label.upper() for keyword in keywords):
                val = df[df.columns[1]].tolist()[labels.index(label)] # find value corresponding to matched label
                arr.append(val*multiplier)
                found = True
                break
        if not found:
            arr.append('NaN')

    #display(df)
    return arr

income_arr = []
for i, file in enumerate(files):
    print(f'Parsing {i+1} of {len(files)} files: '+file)
    if isfile(join(load_path,file)):
        ticker = file.split('.')[0].split('_')[0]
        file_type = file.split('.')[0].split('_')[1]
        df = pd.read_csv(load_path+file)
        if file_type=='income':
            income_arr.append(parse_income(income_headers,ticker,df))

income_numpy = np.array(income_arr)
income_df = pd.DataFrame(income_numpy,columns=['Ticker']+income_headers)

display(income_df)
#income_df.to_csv(save_path+f'Fundamentals_{year}.csv',index=False)