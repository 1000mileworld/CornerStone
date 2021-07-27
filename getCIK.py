import requests
from utilities import save_obj

target_url = 'https://www.sec.gov/include/ticker.txt'
response = requests.get(target_url)
data = response.text.splitlines()

ticker2cik = {}
for line in data:
    ticker = line.split('\t')[0].upper()
    cik = line.split('\t')[1]
    ticker2cik[ticker] = cik

save_obj(ticker2cik, "cik_map")

#print(ticker2cik)