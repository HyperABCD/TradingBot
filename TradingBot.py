import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt
import datetime as dt

df = yf.download("AAPL", start="2010-01-5", end=dt.datetime.now(), interval='1d')

def stocktraitement(df):
    del df['Close']
    df.rename(columns={'Adj Close': 'Close'}, inplace=True)
    df['Close'] = pd.to_numeric(df['Close'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Open'] = pd.to_numeric(df['Open'])
    df['Volume'] = pd.to_numeric(df['Volume'])
    df['ATR12'] = ta.volatility.AverageTrueRange(high=df['High'],low=df['Low'],close=df['Close'],window=12).average_true_range()
    df['ATR11'] = ta.volatility.AverageTrueRange(high=df['High'],low=df['Low'],close=df['Close'],window=11).average_true_range()
    df['ATR10'] = ta.volatility.AverageTrueRange(high=df['High'],low=df['Low'],close=df['Close'],window=10).average_true_range()
    df['SMA50'] = ta.trend.sma_indicator(df['Close'], 50,fillna=False)
    df['MACD'] = ta.trend.macd(df['Close'], window_slow=26, window_fast=12, fillna=False)
    df['MACD_SIGNAL'] = ta.trend.macd_signal(df['Close'], window_slow=26, window_fast=12, fillna=False)
    multiplier3 = 3
    multiplier2 = 2
    multiplier1 = 1
    df['Supertrend 12/3']=(df['High']+df['Low'])/2+(multiplier3)*(df['ATR12'])
    df['Supertrend 11/2']=(df['High']+df['Low'])/2+(multiplier2)*(df['ATR11'])
    df['Supertrend 10/1']=(df['High']+df['Low'])/2+(multiplier1)*(df['ATR10'])
    print(df)
    df.dropna(inplace = True)
    print(df)
    plt.plot(df['Close'])
    plt.show()
 
    return df

df = stocktraitement(df)

def tradingstrategy(df):
    stock = 0
    usd = 100000
    buys = []
    sells = []
    for i in range(len(df)):
        if usd >= 0.001 and  df['SMA50'][i] > df['Close'][i] :
            stock = usd / df['Close'][i]
            print("Buy at:", df['Close'][i])
            usd = 0
            buys.append(df['Close'][i])
        elif stock >= 0.001 and df['SMA50'][i] < df['Close'][i] :
            usd = stock * df['Close'][i]
            print("Sold at:", df['Close'][i])
            stock = 0
            sells.append(df['Close'][i])

    # Afficher le résultat des transactions
    print("Number of buys:", len(buys))
    print("Number of sells:", len(sells))
    print("Final USD balance:", usd + stock * df['Close'].iloc[-1])
    if len(buys) > 0:
        print("Average Buy Price:", sum(buys) / len(buys))
    if len(sells) > 0:
        print("Average Sell Price:", sum(sells) / len(sells))
    return

tradingstrategy(df)

