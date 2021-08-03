from utilities import load_obj
import pandas as pd
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from IPython.display import display

year = 2015
load_path = f"Data\Reports\{year}\\"
save_path = f"Data\Reports Parsed\{year}\\"

def parse_10k(s_data, save_path, type):

    data = s_data['data']
    df = pd.DataFrame(data)
    
    if type=='income' or type=='cash flow':
        headers = s_data['headers'][1] #use 2nd row from table as headers
    else:
        headers = s_data['headers'][0][1:] #first element is index name, not a header
    
    # Define the Index column, rename it, and we need to make sure to drop the old column once we reindex.
    df.index = df[0]
    df.index.name = s_data['headers'][0][0]
    df = df.drop(0, axis = 1)

    # Get rid of the '$', '(', ')', and convert the '' to NaNs.
    df = df.replace('[\$,)]','', regex=True )\
            .replace( '[(]','-', regex=True)\
            .replace( '', 'NaN', regex=True)

    # everything is a string, so let's convert all the data to a float.
    df = df.astype(float)

    # Change the column headers
    df.columns = headers

    # display(income_df)

    # drop the data in a CSV file if need be.
    df.to_csv(save_path+s_data['ticker']+f'_{type}.csv')

#make array of files in directory for easier debugging
files = listdir(load_path)

files = files[22:]

statements_data = []
for i, file in enumerate(files):
    print(f'Parsing {i+1} of {len(files)} files: '+file)
    if isfile(join(load_path,file)):
        
        ticker = file.split('_')[0]
        type = file.split('_')[1].split('.')[0]
        with open(load_path+file) as f:
            report = f.read()
        report_soup = BeautifulSoup(report,'lxml')
        s_data = {}
        s_data['ticker'] = ticker
        s_data['type'] = type
        s_data['headers'] = []
        s_data['sections'] = []
        s_data['data'] = []

        # Storing parsed data in dict
        for index, row in enumerate(report_soup.table.find_all('tr')):
            cols = row.find_all('td')
            # if it's a regular row and not a section or a table header (no th or strong tags)
            if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0): 
                #reg_row = [ele.text.strip() for ele in cols] # see list comprehension for syntax
                reg_row = []
                for ele in cols:
                    #if not ele['class'][0]=='pl' and not ele['class'][0]=='nump':
                    if ele.has_attr('class'):
                        if ele['class'][0]=='fn':
                            continue
                    else:
                        continue
                    soup = BeautifulSoup(str(ele),'lxml')
                    for tag in soup.find_all('span'):
                        tag.replaceWith('')
                    reg_row.append(soup.text.strip())
                s_data['data'].append(reg_row)

            
            # if it's a regular row and a section but not a table header
            elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
                sec_row = cols[0].text.strip()
                s_data['sections'].append(sec_row)
                
            # finally if it's not any of those it must be a header
            elif (len(row.find_all('th')) != 0):            
                hed_row = [ele.text.strip() for ele in row.find_all('th')]
                s_data['headers'].append(hed_row)
                
            else:            
                print('We encountered an error while parsing a table row.')
        
        # Parsing data based on type
        if type=='balance':
            parse_10k(s_data, save_path, 'balance')
        elif type=='income':
            parse_10k(s_data, save_path, 'income')
        elif type=='cash flow':
            parse_10k(s_data, save_path, 'cash flow')
        elif type=='equity':
            parse_10k(s_data, save_path, 'equity')
        else:
            print(f'Unknown report type found: {type}')


#print(Symbols)



