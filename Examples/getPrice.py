import finpie
import pandas as pd

save_path = f"Data\Price\\"

nasdaq = pd.read_csv("tickers.csv")

Symbols = nasdaq['Symbol'].tolist()

#Symbols = Symbols[:1]
Symbols = ['AAPL']

for i,ticker in enumerate(Symbols):
    print(f'Getting price data for {i+1} of {len(Symbols)} ({ticker}):')

    #try:
    df = finpie.historical_prices(ticker)
    df.to_csv(save_path+f'{ticker}_price.csv')
    # except:
    #     print("No price data found!")