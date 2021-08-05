# download specific reports from SEC

from json import load

from requests.api import get
from utilities import load_obj, get_url

year = 2016
load_path = "Data\Objects\\"
save_path = f"Data\Reports\{year}\\"

report_urls = load_obj(f'{load_path}report_urls_{year}')
Symbols = list(report_urls.keys())

#Symbols = Symbols[2410:]
#Symbols = ['AAPL']
for i,ticker in enumerate(Symbols):
    print('-'*100)
    print(f'Downloading reports for {i+1} of {len(Symbols)} tickers ({ticker})...')
    for type in report_urls[ticker]:
        print(f'Downloading {type.upper()} report for {ticker}: '+report_urls[ticker][type])
        content = get_url(report_urls[ticker][type],'content')
        f = open(save_path+ticker+f'_{type}'+".html", "wb")
        f.write(content)
        f.close()