import yfinance as yf
import pandas as pd 
import datetime


today = datetime.date.today()
start = today -  datetime.timedelta(days=25)

print(today)
print(start)