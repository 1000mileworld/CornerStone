# How to Web Scrape the SEC | Part 2
# https://www.youtube.com/watch?v=eut8-iOiJ_Q

# scrape SEC by quarter
# master filing list exists for every business day of quarter

import requests
import time
import urllib
from bs4 import BeautifulSoup

def make_url(base_url,comp):
    url = base_url
    for r in comp:
        url = '{}/{}'.format(url,r)

    return url

def get_url(url):
    content = requests.get(url)
    count = 0
    while content.status_code!=200: # keep trying until server says ok
        count+=1
        time.sleep(5)
        content = requests.get(url)
    if count>1:
        print(f'Success after {count} tries!')
    return content.json()


base_url = r"https://www.sec.gov/Archives/edgar/daily-index"

# create daily index url for 2019
year_url = make_url(base_url,['2019','index.json'])

print('Retrieving 2019 links...')
decoded_content = get_url(year_url)

for item in decoded_content['directory']['item']:
    print('-'*100)
    print('Pulling url for quarter {}'.format(item['name']))

    #create quarter url
    qtr_url = make_url(base_url,['2019',item['name'],'index.json'])
    print(qtr_url)

    # file_content = requests.get(qtr_url)
    # decoded_content = file_content.json()

    decoded_content = get_url(qtr_url)

    print('-'*100)
    print('Pulling files')

    for file in decoded_content['directory']['item']:
        file_url = make_url(base_url,['2019',item['name'],file['name']])
        print(file_url)