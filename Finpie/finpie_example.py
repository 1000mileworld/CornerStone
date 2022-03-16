import finpie # or import finpie.fundamental_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
metrics:
-revenue/sales: fd.income_statement()
-net income/earnings: fd.income_statement()
-market capital: nasdaq screener
-market sector: nasdaq screener
-shares outstanding: fd.income_statement()
-Cash flow = Cash_flow_from_operating_activities +(-) cash_flow_from_investing_activities + cash_flow_from_financial_activities	(fd.cashflow_statement())
-Shareholder yield: fd.cashflow_statement()
    -total_common_and_preferred_stock_dividends_paid	
    -net share repurchases: net_total_equity_issued_to_repurchased
    -net debt repayment: debt_issuance_to_retirement_net__total
    -returned capital: add everything, multiply by -1 (cash outflow is negative, but that's the capital given to shareholders)
    -shareholder yield = returned capital divided by market capitalization
"""
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--hide-scrollbars')
# options.add_argument('--disable-gpu')
# options.add_argument("--log-level=3")  # fatal
# driver = webdriver.Chrome(options=options)
# must download chrome driver and add it to PATH
# chrome and chrome driver has to be the same version


# other options:
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(options=options)

# options = Options()
# options.headless = True
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# driver = webdriver.Chrome(options=options)

# default:
# source = 'macrotrends'
# freq = 'A'

df = finpie.nasdaq_tickers()
# df.to_csv('tickers.csv')
print(df.head(10))

# ticker = 'AAPL'
# print(f'Getting data on {ticker}...')
# fd = finpie.Fundamentals(ticker, source = 'macrotrends', freq = 'A')
#df = fd.income_statement() #webdriver options need to be put in here
#df.to_csv(f'{ticker}_income.csv')
# df=fd.key_metrics()
# df.to_csv(f'{ticker}_keyMetrics.csv')
#print('Done!')



# source options for financial statements and key metrics:
# 'yahoo', 'marketwatch', 'macrotrends'
# freq options:
# 'A', 'Q'

# default key metrics for marketwatch and macrotrends come from Finviz