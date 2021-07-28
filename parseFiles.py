# Parse files from Filing Summary URL

year = 2015
Symbols = ['AAPL']

for ticker in Symbols:

    with open(f"Data\Filing Summaries\{year}\\"+ticker+"_url.txt") as f:
        summary_url = f.read()

    print(summary_url)