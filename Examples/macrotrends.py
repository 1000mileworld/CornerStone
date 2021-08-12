import finpie # or import finpie.fundamental_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
metrics:
-revenue/sales: income_statement
-net income/earnings: income_statement
-market capital: nasdaq screener
-market sector: nasdaq screener
-shares outstanding: income_statement
-cash flow: 
-shareholder yield:
"""
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--hide-scrollbars')
# options.add_argument('--disable-gpu')
# options.add_argument("--log-level=3")  # fatal

# # must download chrome driver and add it to PATH
# # chrome and chrome driver has to be the same version
# driver = webdriver.Chrome(options=options)

# default:
# source = 'macrotrends'
# freq = 'A'
ticker = 'AAIC'

print(f'Getting data on {ticker}...')


fd = finpie.Fundamentals(ticker, source = 'macrotrends', freq = 'A')
df = fd.income_statement()
df.to_csv(f'{ticker}_income.csv')

print('Done!')

# source options for financial statements and key metrics:
# 'yahoo', 'marketwatch', 'macrotrends'
# freq options:
# 'A', 'Q'

# default key metrics for marketwatch and macrotrends come from Finviz