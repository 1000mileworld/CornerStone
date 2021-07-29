from utilities import load_obj

year = 2015
save_path = f"Data\Reports\{year}\\"
ticker_info = load_obj('ticker_info')

report_list = [
    r"Consolidated Balance Sheets",
    r"Consolidated Statements of Operations and Comprehensive Income (Loss)",
    r"Consolidated Statements of Cash Flows",
    r"Consolidated Statements of Stockholder's (Deficit) Equity"
    ]
for i in range(len(report_list)):
    report_list[i] = report_list[i].upper()

Symbols = []
for item in list(ticker_info.items()):
    Symbols.append(item[0])

statements_url = {}
Symbols = Symbols[:3]
for i, ticker in enumerate(Symbols):
    print('-'*100)
    print(f'Getting reports for {i+1} of {len(Symbols)} tickers ({ticker}): '+ticker_info[ticker]['base_url'])
    for report_dict in ticker_info[ticker]['reports']:
        report = report_dict['name_short'].upper()
        if report in report_list:
            print('Downloading '+report_dict['name_short']+': '+report_dict['url'])
