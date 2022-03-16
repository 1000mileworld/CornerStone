# Web Scraping Fundamentals Data for Corner Stone Growth/Value Strategies
The Corner Stone Growth/Value strategies come from the book, "What Works on Wall Street", by James P. O'Shaughnessy. The strategies rely on analyzing a company's fundamentals in order to predict its stock's future performance. Getting access to quality fundamental data may be quite expensive for the average investor, and this code offers 2 methods of using freely available data to build your own database of fundamentals.

## Method 1: Scrape 10-K filings from the Security Exchange Commission (SEC) website and use the data to calculate fundamentals
1. Manually download stock list csv from [NASDAQ stock screener](https://www.nasdaq.com/market-activity/stocks/screener)
2. Download historical prices for each stock from Yahoo Finance (downloadYF.py)
3. Generate a [map of ticker symbol to CIK](https://www.sec.gov/include/ticker.txt) for downloading from SEC and save to dictionary structure (getCIK.py)
4. Use CIK map to download "Filing Summary.xml" for each ticker from SEC (downloadSummaries.py)
5. From each filing summary, get all report links and save all URLs (getReportLinks.py)
6. For each ticker, find a URL for each type of report (ex. ‘balance’, ‘income’, etc.) and save specific report URLs (checkReportLinks.py)
7. Download reports (financial statements), saved as .html (downloadReports.py)
8. Parse each table in report (html format) and save data to csv (parseReports.py)
9. Fundamentals can be calculated from the downloaded data. However, 10-K filings from different companies may use slightly different formatting so parsing them can be challenging (see MATLAB folder)

## Method 2: Use Finpie library to get fundamental data directly
1. After getting data from yfinance, filter price data for stocks which has data for most trading days of the year (ignore stocks that have too many days without price data)
2. Set up download directories, log and ticker position text files (initialize.py)
3. Calls multiple instances (4-5 seems to be most stable) of getStatements.py to download fundamental data in parallel (manager.py)
4. Automate manager.py. For Windows, use Windows scheduler to run manager.py on restart (in case of losing internet connection, see Readme.docx for more details)
5. After finish downloading, need to check all income statements are downloaded for every cashflow statement downloaded (checkIncome.py)
6. Check if any tickers aren't downloaded at all as sometimes the connection may be bad (findMissing.py) 
7. Download any missing symbols (manager.py)

Method 2 is preferred since you don't have to parse various 10-K formatting and calculate fundamentals yourself, unless there's a metric that is not readily available. However, the source for Method 1 ([SEC.gov](https://www.sec.gov/)) is probably more robust than a Python library that depends on several additional external data sources.

Simulation of the Corner Stone strategies is done in MATLAB. Of course, the data can also be used to test other strategies.
