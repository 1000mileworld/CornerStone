# Get all report links for each ticker from its Filing Summary.xml
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from utilities import save_obj

year = 2015
mypath = f"Data\Filing Summaries\{year}\\"
#Symbols = [f.split('.')[0] for f in listdir(mypath) if isfile(join(mypath, f))]

# docs = [
#     r"Consolidated Balance Sheets",
#     r"Consolidated Statements of Operations and Comprehensive Income (Loss)",
#     r"Consolidated Statements of Cash Flows",
#     r"Consolidated Statements of Stockholder's (Deficit) Equity"
#     ]

Symbols = []
ticker_info = {} #base + docs URLs for each ticker

print("Getting ticker symbols and base URLs...")
for f in listdir(mypath):
    if isfile(join(mypath,f)):
        if f.split('.')[1] == 'txt':
            ticker = f.split('.')[0].split('_')[0]
            with open(mypath+f) as f_url:
                summary_url = f_url.read()
            ticker_info[ticker] = {}
            ticker_info[ticker]['base_url'] = summary_url
            Symbols.append(ticker)

#Symbols = Symbols[:10]
for i,ticker in enumerate(Symbols):
    print(f'Retrieving report URLS for {i+1} of {len(Symbols)} ({ticker})')
    try:
        with open(mypath+ticker+'.xml','rb') as f_xml:
            soup = BeautifulSoup(f_xml,'lxml')
    except OSError as e:
        print(f'No xml file found for {ticker}!')
        continue
    
    reports = soup.find('myreports')
    ticker_info[ticker]['reports'] = []
    for report in reports.find_all('report')[:-1]: # last report has different format than rest
        report_dict = {}
        report_dict['name_short'] = report.shortname.text
        report_dict['name_long'] = report.longname.text
        #report_dict['position'] = report.position.text
        #report_dict['category'] = report.menucategory.text
        report_dict['url'] = ticker_info[ticker]['base_url'] + report.htmlfilename.text

        # append the dictionary to the master list
        ticker_info[ticker]['reports'].append(report_dict)

        # print the info to the user.
        # print('-'*100)
        # print(report_dict['url'])
        # print(report_dict['name_long'])
        # print(report_dict['name_short'])
        # print(report_dict['category'])
        # print(report_dict['position'])

save_obj(ticker_info,'ticker_info')
print('Report URLS retrieved and saved.')