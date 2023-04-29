import yfinance as yf
import pandas as pd 


def get_previous_close(ticker:str) -> float:
    """returns the previous closing price for the stock using y.finance, given ticker"""
    stock = yf.Ticker(ticker)
    price = stock.history(period='5d').Close.backfill().iloc[-1]
    return price    


print(get_previous_close('MSFT'))