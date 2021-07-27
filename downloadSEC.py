import utilities
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

Symbols = ['AAPL']

cikMap = utilities.load_obj("cik_map")
#base_url = r"https://www.sec.gov/Archives/edgar/data"
endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"
base_url_sec = r"https://www.sec.gov"

for ticker in Symbols:
    if ticker in cikMap:
        cik_num = cikMap[ticker]
        param_dict = {'action':'getcompany',
              'CIK': cik_num,
              'type':'10-k',
              'dateb':'20160101',
              'owner':'exclude',
              'start':'',
              'output':'',
              'count':'100'}

        print(f"Getting URL for {ticker}")
        response = requests.get(url = endpoint, params = param_dict)
        count = 1
        while response.status_code!=200: # keep trying until server says ok
            count+=1
            time.sleep(5)
            response = requests.get(url = endpoint, params = param_dict)
        if count>1:
            print(f'Success after {count} tries!')
        
        print(response.url)
        # filings_url = utilities.make_url(base_url, [cik_num, 'index.json'])
        # decoded_content = utilities.get_url(filings_url)
        # print(json.dumps(decoded_content, indent=4))

        #-----------Parse response for document details------------------
        soup = BeautifulSoup(response.content, 'html.parser')
        doc_table = soup.find_all('table', class_='tableFile2')
        master_list = []
        # loop through each row in the table.
        for row in doc_table[0].find_all('tr')[0:3]: #first 4 rows including table header
            
            # find all the columns
            cols = row.find_all('td')
            
            # if there are no columns move on to the next row.
            if len(cols) != 0:        
                
                # grab the text
                filing_type = cols[0].text.strip()                 
                filing_date = cols[3].text.strip()
                filing_numb = cols[4].text.strip()
                
                # find the links
                filing_doc_href = cols[1].find('a', {'href':True, 'id':'documentsbutton'})       
                filing_int_href = cols[1].find('a', {'href':True, 'id':'interactiveDataBtn'})
                filing_num_href = cols[4].find('a')
                
                # grab the the first href
                if filing_doc_href != None:
                    filing_doc_link = base_url_sec + filing_doc_href['href'] 
                else:
                    filing_doc_link = 'no link'
                
                # grab the second href
                if filing_int_href != None:
                    filing_int_link = base_url_sec + filing_int_href['href'] 
                else:
                    filing_int_link = 'no link'
                
                # grab the third href
                if filing_num_href != None:
                    filing_num_link = base_url_sec + filing_num_href['href'] 
                else:
                    filing_num_link = 'no link'
                
                # create and store data in the dictionary
                file_dict = {}
                file_dict['file_type'] = filing_type
                file_dict['file_number'] = filing_numb
                file_dict['file_date'] = filing_date
                file_dict['links'] = {}
                file_dict['links']['documents'] = filing_doc_link
                file_dict['links']['interactive_data'] = filing_int_link
                file_dict['links']['filing_number'] = filing_num_link
            
                # let the user know it's working
                print('-'*100)        
                print("Filing Type: " + filing_type)
                print("Filing Date: " + filing_date)
                print("Filing Number: " + filing_numb)
                print("Document Link: " + filing_doc_link)
                print("Filing Number Link: " + filing_num_link)
                print("Interactive Data Link: " + filing_int_link)
                
                # append dictionary to master list
                master_list.append(file_dict)