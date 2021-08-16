import finpie
from os import listdir
from os.path import isfile, join

year = 2020

load_path = f"..\Data\Prices\{year}\\"
save_path = f"Data\\"

Symbols = [f.split('.')[0] for f in listdir(load_path) if isfile(join(load_path, f))]
Symbols = Symbols[50:]
#Symbols = ["ACEVU"]

for i,ticker in enumerate(Symbols):
    print(f'Getting data for {i+1} of {len(Symbols)} ({ticker}):')
    fd = finpie.Fundamentals(ticker, source = 'macrotrends', freq = 'A')
    
    print("Downloading cashflow statement...")
    try:
        df1 = fd.cashflow_statement()
        df1.to_csv(save_path+f'Cashflow\{ticker}_cashflow.csv')
    except:
        print("No data found!")
        continue

    print("Downloading income statement....")
    try:
        df2 = fd.income_statement()
        df2.to_csv(save_path+f'Income\{ticker}_income.csv')
    except:
        print("No data found!")
        continue

print("Done!")
