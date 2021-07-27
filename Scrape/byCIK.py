# How to Web Scrape the SEC | Part 1
# https://www.youtube.com/watch?v=-7I7OAC6ih8

import requests
from bs4 import BeautifulSoup
from utilities import get_url

base_url = r"https://www.sec.gov/Archives/edgar/data"
cik_num = '/886982/' #Goldman Sachs
filings_url = base_url + cik_num + "index.json"

print("Getting all filings for company...")
decoded_content = get_url(filings_url)

# grab single filing number
filing_number = decoded_content['directory']['item'][0]['name']
filing_url = base_url + cik_num + filing_number + "/index.json"

print("Getting single filing for company...")
document_content = get_url(filing_url)

# get document names
for document in document_content['directory']['item']:
    if document['type']!='image2.gif':
        doc_name = document['name']
        document_url = base_url + cik_num + filing_number + "/" + doc_name
        print(document_url)