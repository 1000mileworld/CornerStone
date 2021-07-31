# Check if report links exist for the report types desired and save
from utilities import load_obj, save_obj

ticker_info = load_obj('ticker_info')

report_types = ['balance','income','cash flow','equity']
#report_types = ['equity']
report_urls = {}

# report_list = [
#     r"Consolidated Balance Sheets",
#     r"Consolidated Statements of Operations and Comprehensive Income (Loss)",
#     r"Consolidated Statements of Cash Flows",
#     r"Consolidated Statements of Stockholder's (Deficit) Equity"
#     ]
# for i in range(len(report_list)):
#     report_list[i] = report_list[i].upper()

Symbols = []
for item in list(ticker_info.items()):
    Symbols.append(item[0])

#Symbols = Symbols[:3]
#Symbols = ['ENBL']
url_check = {}
for i, ticker in enumerate(Symbols):
    print('-'*100)
    print(f'Getting reports for {i+1} of {len(Symbols)} tickers ({ticker}): '+ticker_info[ticker]['base_url']+'FilingSummary.xml\n') 
    url_check[ticker] = {}
    report_urls[ticker] = {}
    for type in report_types:
        url_check[ticker][type] = 0
        if type=='balance':
            for report_dict in ticker_info[ticker]['reports']:
                name_long = report_dict['name_long'].upper()
                keywords = ["FINANCIAL POSITION", "FINANCIAL CONDITION", "BALANCE SHEET", "STATEMENTS OF CONDITION",
                            "ASSETS, LIABILITIES AND EQUITY"]
                forbidden = ["PAR","THETICAL","DISCLOSURE", "LP CUBE","NOTE", "FIRSTENERGY SOLUTIONS CORP.","PHANTOM"]
                if any(keyword in name_long for keyword in keywords):
                    if not any(word in name_long for word in forbidden) and "STATEMENT" in name_long:
                        if url_check[ticker][type]<1:
                            print(report_dict['name_short']+': '+report_dict['url'])
                            url_check[ticker][type]+=1
        elif type=='income':
            for report_dict in ticker_info[ticker]['reports']:
                name_long = report_dict['name_long'].upper()
                keywords = ["COMPREHENSIVE INCOME","OF INCOME","OF OPERATIONS","COMPREHENSIVE LOSS","CONSOLIDATED INCOME",
                            "COMPREHENSIVE EARNINGS","STATEMENTS OF EARNINGS","CONSOLIDATED OPERATIONS"]
                forbidden = ["PAR","THETICAL","DISCLOSURE"]
                if any(keyword in name_long for keyword in keywords):
                    if not any(word in name_long for word in forbidden) and "STATEMENT" in name_long:
                        if url_check[ticker][type]<1:
                            print(report_dict['name_short']+': '+report_dict['url'])
                            url_check[ticker][type]+=1
        elif type=='cash flow':
            for report_dict in ticker_info[ticker]['reports']:
                name_long = report_dict['name_long'].upper()
                keywords = ["CASH FLOW","OF CASHFLOW"]
                forbidden = ["PAR","THETICAL","DISCLOSURE","SCHEDULE","CONTINUED"]
                if any(keyword in name_long for keyword in keywords):
                    if not any(word in name_long for word in forbidden) and "STATEMENT" in name_long:
                        if url_check[ticker][type]<1:
                            print(report_dict['name_short']+': '+report_dict['url'])
                            url_check[ticker][type]+=1
        elif type=='equity':
            for report_dict in ticker_info[ticker]['reports']:
                name_long = report_dict['name_long'].upper()
                keywords = ["STOCKHOLDER","SHAREHOLDER","EQUITY","EQUITIES","CAPITAL","BENEFICIAR",
                            "DEFICIT", "SHAREOWNER"]
                forbidden = ["PARENTH","THETICAL","DISCLOSURE"]
                #temp = "00500 - Statement - CONSOLIDATED STATEMENT OF PARTNERS' CAPITAL"
                #if name_long==temp.upper():
                #    a=4
                if any(keyword in name_long for keyword in keywords):
                    if not any(word in name_long for word in forbidden) and "STATEMENT" in name_long:
                        if url_check[ticker][type]<1:
                            print(report_dict['name_short']+': '+report_dict['url'])
                            report_urls[ticker][type] = report_dict['url']
                            url_check[ticker][type]+=1
        else:
            print(f'Unrecognized report type requested for {ticker}: {type}')

print('*'*50+'ERROR CHECKING'+'*'*50)
print("Checking each report type for a ticker has exactly one URL...")
error_found = False

#exceptions = ['BDX','BMY','CVR','DVD','EMN','GTY']
exceptions=[]
for ticker in url_check:
    if not ticker in exceptions:
        for type in url_check[ticker]:
            if url_check[ticker][type]==0:
                print(f'No reports of type {type.upper()} found for {ticker}: '+ticker_info[ticker]['base_url']+'FilingSummary.xml')
                error_found = True
            elif url_check[ticker][type]>1:
                print(f'Multiple reports of type {type.upper()} found for {ticker}: '+ticker_info[ticker]['base_url']+'FilingSummary.xml')
                error_found = True

if not error_found:
    print("No errors found!")

save_obj(report_urls,"report_urls")