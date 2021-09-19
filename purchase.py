import alpaca_trade_api as tradeapi
import numpy as np

#paper api keys
API_KEY = "PK790DLZRZT4YKVM4SHK"
API_SECRET = "OTQ75hKD4fWOyjLfHvSb29f6i1YDPpwQRpHeDSwn"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

load_path = "MATLAB\\"
numStocks = 25
splits = [0.5, 0.5] #portfolio % for [growth, value]

def simBuy(Symbols,funds,api):
    capital = funds
    counter = 0
    portfolio = {}

    for ticker in Symbols:
        portfolio[ticker] = 0

    while capital>0:
        ticker = Symbols[counter]
        barset = api.get_barset(ticker, 'day', limit=1)
        price = barset[ticker][0].c #simulate with previous day's closing price
        
        if price>capital:
            break

        portfolio[ticker]+=1
        capital-=price

        if counter==len(Symbols)-1:
            counter=0
        else:
            counter+=1
    
    return portfolio

def sellAll(api):
    portfolio = api.list_positions()
    for position in portfolio:
        api.submit_order(position.symbol,position.qty,'sell','market','day')

def combinePort(port1,port2): #combine 2 portfolio strategies
    portfolio = port1
    for ticker in port2:
        if ticker in port1:
            portfolio[ticker]+=port2[ticker]
        else:
            portfolio[ticker] = port2[ticker]
    return portfolio


api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()
equity = float(account.equity)

s_growth = np.loadtxt(load_path+"growth.txt",dtype='str').tolist()[:numStocks]
s_val = np.loadtxt(load_path+"value.txt",dtype='str').tolist()[:numStocks]

p_growth = simBuy(s_growth,splits[0]*equity,api)
p_val = simBuy(s_val,splits[1]*equity,api)
p_goal = combinePort(p_growth,p_val) #portfolio should look like this when done

portfolio = api.list_positions()
if len(portfolio)>0: #stocks already present
    p_current = []
    for position in portfolio: #check which positions are on the list
        ticker = position.symbol
        if ticker in p_goal: #match stock quantity to desired
            p_current.append(ticker)
            quantity = p_goal[ticker]-int(position.qty)
            if quantity>0:
                api.submit_order(ticker,quantity,'buy','market','day')
            elif quantity<0: #only sell what's needed (tax efficiency)
                api.submit_order(ticker,-quantity,'sell','market','day')
        else:
            api.submit_order(ticker,position.qty,'sell','market','day')
    
    #buy stocks on the list but avoid duplicates
    for ticker in p_goal:
        if not ticker in p_current:
            api.submit_order(ticker,p_goal[ticker],'buy','market','day')
else: #first time running script, no positions open
    for ticker in p_goal:
        api.submit_order(ticker,p_goal[ticker],'buy','market','day')