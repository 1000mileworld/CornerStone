from os import listdir
from os.path import isfile, join
import requests
import numpy as np

year = 2020

origin_path = f"..\Data\Prices\{year}\\"
statements_path = f"Data\\"
base_url = "https://www.macrotrends.net/stocks/charts/"
outfile = "Missing Symbols.txt"

s_origin = [f.split('.')[0] for f in listdir(origin_path) if isfile(join(origin_path, f))]
s_statements = [f.split('_')[0] for f in listdir(statements_path+"Income") if isfile(join(statements_path+"Income", f))]

s_origin = s_origin[:1916]

# s_origin = ["aapl"]
# for i,ticker in enumerate(s_origin):
#     print(f'Checking stock {i+1} of {len(s_origin)} ({ticker})...')

#     url = base_url+ticker
#     response = requests.get(url)
#     if response.history:
#         # Request was redirected, status code 301
#         print(response.url)

s_missing = []
for i,ticker in enumerate(s_origin):
    if not ticker in s_statements:
        s_missing.append(ticker)

#print(s_missing)
s_missing_np = np.array(s_missing)
with open(outfile, 'w') as f:
    np.savetxt(outfile,s_missing_np,fmt='%s')

loaded = np.loadtxt(outfile,dtype='str')
print(loaded.tolist())