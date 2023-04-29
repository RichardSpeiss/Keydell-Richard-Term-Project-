import pandas as pd
import yfinance as yf
import numpy as np
import time
import yfinance as yf

# List of stock tickers
tickers = ["AAPL", "GOOG", "TSLA", "NVDA", "MSFT", "AMZN"]

# Fetch data for multiple tickers
data = yf.Tickers(tickers)

# Access data for each ticker
for ticker in tickers:
    print(ticker, data.tickers[ticker].info["recommendationKey"])

    # try:
    #     info = ticker.info
    #     recommendation = info['recommendationMean']
    # except:
    #     recommendation = 6

    # recommendations[tickers[0]] = recommendation

    # print("--------------------------------------------")
    # print("{} has an average recommendation of: {}".format(tickers[0], recommendation))

    # time.sleep(5)

# print(recommendations)
