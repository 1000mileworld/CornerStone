# Parse files from Filing Summary URL
from os import listdir
from os.path import isfile, join

year = 2015

mypath = f"Data\Prices\{year}\\"
Symbols = [f.split('.')[0] for f in listdir(mypath) if isfile(join(mypath, f))]
print(Symbols[0:3])

# Symbols = ['AAPL']

# for ticker in Symbols:

#     with open(f"Data\Filing Summaries\{year}\\"+ticker+"_url.txt") as f:
#         summary_url = f.read()

#     print(summary_url)