import pandas as pd
import matplotlib.pyplot as plt
import ta
import yfinance as yf
import datetime

today = datetime.datetime.now()
today = today.strftime("%Y-%m-%d")
stockname = str(input("Enter Ticker :"))
start_trading_period = str(input("Enter your trading period in format (Y-M-D) :"))
df = yf.download(stockname, start="2007-09-26", end=today,interval = '1d',)

def stocktraitement(df):
    del df['Close']
    df.rename(columns = {'Adj Close':'close'}, inplace = True)
    df['close'] = pd.to_numeric(df['close'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Open'] = pd.to_numeric(df['Open'])
    df['SMA50'] = ta.trend.sma_indicator(df['close'], 50,fillna=False)
    df['MACD'] = ta.trend.macd(df['close'], window_slow=26, window_fast=12, fillna=False)
    df['MACD_SIGNAL'] = ta.trend.macd_signal(df['close'], window_slow=26, window_fast=12, fillna=False)
    print(df)
    return df

df = stocktraitement(df)

def tradingstrategy(df,start_trading_period):
    lastbuyprice = None
    start_trading_period = pd.to_datetime(start_trading_period)
    stock = 0
    usd = 10000
    number_trade = 0
    win_trade = 0
    buys = []
    sells = []
    for i in range(len(df)):
       current_date = df.index.get_level_values(0)[i]
       if current_date >= start_trading_period:
          if lastbuyprice is None:
            if abs(df['MACD_SIGNAL'][i] - df['MACD'][i]) < 0.05 and df['MACD_SIGNAL'][i] < 0 and df['MACD'][i] < 0 and usd > 10:
                buys.append(i)
                stock = usd/df['close'][i]
                usd = 0
                print('Buy at ',df['close'][i],'date: ',df.index.get_level_values(0)[i])
                lastbuyprice = df['close'][i]
          else:
            if  abs(df['MACD_SIGNAL'][i] - df['MACD'][i]) < 0.05 and df['MACD_SIGNAL'][i] > 0 and df['MACD'][i] > 0 or df['close'][i] > lastbuyprice * 1.2 and stock > 0.0001:
                sells.append(i)
                usd = stock*df['close'][i]
                stock = 0
                print('Sell at ',df['close'][i],'date: ',df.index.get_level_values(0)[i])
                number_trade = number_trade+1
                if lastbuyprice * 1.2 > df['close'][i]:
                    win_trade = win_trade+1
                lastbuyprice = None
    print("Number of Trades: ", number_trade)
    print("Number of winning Trades: ", win_trade)
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    today = today.strftime("%Y-%m-%d")
    profit = usd+stock*df.loc[today, "close"]
    print(profit)
    print("Buy and hold result", (10000 / df.loc[start_trading_period,"close"]) *  df.loc[today, "close"],'USDT')
    return buys,sells

buys,sells = tradingstrategy(df,start_trading_period)

def creategraph(df,buys,sells):
    
    for i in buys:
        date = df.index.get_level_values(0)[i]
        plt.axvline(x = date, color = 'b', label = 'axvline - full height')
    for i in sells:
        date = df.index.get_level_values(0)[i]
        plt.axvline(x = date, color = 'r', label = 'axvline - full height')
    plt.axhline(y=0)
    plt.plot(df['close'])
    plt.plot(df['MACD'], color='blue')
    plt.plot(df['MACD_SIGNAL'], color='orange')
    plt.plot(df['SMA50'],color='purple')
    plt.show()

creategraph(df,buys,sells)
