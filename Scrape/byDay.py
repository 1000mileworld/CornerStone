# How to Web Scrape the SEC | Part 2
# find all filings for given day of the year (such as 10K forms)
# https://www.youtube.com/watch?v=eut8-iOiJ_Q

import requests

# file_url = r"https://www.sec.gov/Archives/edgar/daily-index/2019/QTR2/master.20190401.idx"

# content = requests.get(file_url).content

# wb means write in binary mode
# with open('master_20190401.txt','wb') as f:
#     f.write(content)

# read content
with open('master_20190401.txt','rb') as f:
    byte_data = f.read()

# decode byte data
data = byte_data.decode('utf-8').split('  ')

# finding the starting index
for index, item in enumerate(data):
    if 'ftp://ftp.sec.gov/edgar/' in item:
        start_ind = index

# create a new list that removes the junk
data_format = data[start_ind+1:]
# print(str(data_format)[1:500])

master_data = []
for index, item in enumerate(data_format):
    if index==0:
        clean_item_data = item.replace('\n','|').split('|')
        clean_item_data = clean_item_data[8:]
    else:
        clean_item_data = item.replace('\n','|').split('|')

    for index, row in enumerate(clean_item_data):
        if '.txt' in row:
            mini_list = clean_item_data[(index-4): index+1]
            
            if len(mini_list) != 0:
                mini_list[4] = "https://www.sec.gov/Archives/"+mini_list[4]
                master_data.append(mini_list)
                #print(mini_list)

#print(master_data[:3])

#restructure
for index, document in enumerate(master_data):
    #create dictionary
    document_dict = {}
    document_dict['cik_number'] = document[0]
    document_dict['company_name'] = document[1]
    document_dict['form_id'] = document[2]
    document_dict['date'] = document[3]
    document_dict['file_url'] = document[4]

    master_data[index] = document_dict

for document_dict in master_data:
    if document_dict['form_id'] == '10-K':
        print(document_dict['company_name'])
        print(document_dict['file_url'])