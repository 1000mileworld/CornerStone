# How to Web Scrape the SEC | Part 3
# https://www.youtube.com/watch?v=4zE9HjPIqC4
# parse financial info from 10K forms

import requests
import pandas as pd
from bs4 import BeautifulSoup
from utilities import get_url, load_obj
import json
from IPython.display import display

base_url = r"https://www.sec.gov"

# convert a normal url to a document url (for 10K)
normal_url = r"https://www.sec.gov/Archives/edgar/data/1265107/0001265107-19-000004.txt"
documents_url = normal_url.replace('-','').replace('.txt','/index.json')
#print(document_url)

# content = get_url(documents_url)
with open('json-004.json') as f: #saved json file to avoid requesting url
    content = json.load(f)

for file in content['directory']['item']:
    # Grab filing summary and create new url leading to the file so we can download it
    if file['name']=='FilingSummary.xml':
        xml_summary = base_url+content['directory']['name']+'/'+file['name']
        print('-'*100)
        print('File Name: '+file['name'])
        print('File Path: '+xml_summary)
        break

base_url = xml_summary.replace('FilingSummary.xml','')
# content = get_url(xml_summary,'content')

with open('FilingSummary.xml') as f: #saved xml file
    soup = BeautifulSoup(f,'lxml')

# find the 'myreports' tag because this contains all the individual reports submitted.
reports = soup.find('myreports') # my reports not case sensitive if using lxml to parse

master_reports = []

for report in reports.find_all('report')[:-1]: # last report has different format than rest
    report_dict = {}
    report_dict['name_short'] = report.shortname.text # shortname is a tag in the xml file
    report_dict['name_long'] = report.longname.text
    report_dict['position'] = report.position.text
    report_dict['category'] = report.menucategory.text
    report_dict['url'] = base_url+report.htmlfilename.text

    master_reports.append(report_dict)

    # print('-'*100)
    # print(base_url + report.htmlfilename.text)
    # print(report.longname.text)
    # print(report.shortname.text)
    # print(report.menucategory.text)
    # print(report.position.text)

# --------------------Get url for financial statement docs--------------------
statements_url = []
for report_dict in master_reports:
    # define the statements we want to look for
    item1 = r"Consolidated Balance Sheets"
    item2 = r"Consolidated Statements of Operations and Comprehensive Income (Loss)"
    item3 = r"Consolidated Statements of Cash Flows"
    item4 = r"Consolidated Statements of Stockholder's (Deficit) Equity"

    report_list = [item1,item2,item3,item4]
    if report_dict['name_short'] in report_list:
        print('-'*100)
        print(report_dict['name_short'])
        print(report_dict['url'])
        statements_url.append(report_dict['url'])

#-------------------Build dictionary of financial data found in tables---------------
print('-'*100)
"""
print('Getting financial statements...')
statements_data = []
for statement in statements_url:
    statement_data = {}
    statement_data['headers'] = []
    statement_data['sections'] = []
    statement_data['data'] = []

    content = get_url(statement,'content')
    report_soup = BeautifulSoup(content,'lxml')

    # all data exists in table
    for index, row in enumerate(report_soup.table.find_all('tr')):
        cols = row.find_all('td')

        # if it's a regular row and not a section or a table header (no th or strong tags)
        if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0): 
            reg_row = [ele.text.strip() for ele in cols] # see list comprehension for syntax
            statement_data['data'].append(reg_row)
        
        # if it's a regular row and a section but not a table header
        elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
            sec_row = cols[0].text.strip()
            statement_data['sections'].append(sec_row)
            
        # finally if it's not any of those it must be a header
        elif (len(row.find_all('th')) != 0):            
            hed_row = [ele.text.strip() for ele in row.find_all('th')]
            statement_data['headers'].append(hed_row)
            
        else:            
            print('We encountered an error while parsing a table row.')

    statements_data.append(statement_data)

"""
#------------------Convert Data into Data Frame-----------------------------
# picked example data from Consolidated Statements of Operations and Comprehensive Income (Loss) -> statements_data[1]
statements_data = load_obj('statements data')

income_headers = statements_data[1]['headers'][1] # there are 2 header rows in the income statement, 2nd row is for dates
income_data = statements_data[1]['data']
income_df = pd.DataFrame(income_data)

print('-'*100)
print('Before Reindexing')
print('-'*100)
display(income_df.head())

# Define the Index column, rename it, and we need to make sure to drop the old column once we reindex.
income_df.index = income_df[0]
income_df.index.name = 'Category'
income_df = income_df.drop(0, axis = 1)

# Display
print('-'*100)
print('Before Regex')
print('-'*100)
display(income_df.head())

# Get rid of the '$', '(', ')', and convert the '' to NaNs.
income_df = income_df.replace('[\$,)]','', regex=True )\
                     .replace( '[(]','-', regex=True)\
                     .replace( '', 'NaN', regex=True)

# Display
print('-'*100)
print('Before type conversion')
print('-'*100)
display(income_df.head())

# everything is a string, so let's convert all the data to a float.
income_df = income_df.astype(float)

# Change the column headers
income_df.columns = income_headers

# Display
print('-'*100)
print('Final Product')
print('-'*100)

# show the df
display(income_df)

# drop the data in a CSV file if need be.
# income_df.to_csv('income_state.csv')